import json
import logging
import os
from contextlib import suppress

from jsonschema import validate as json_validate
from prance import ResolvingParser

logging.getLogger("openapi_spec_validator.validators").setLevel(logging.WARNING)


class StaxContract:
    _swagger_doc = None
    _resolved_schema = None

    class ValidationException(Exception):
        def __init__(self, message):
            # logging.info(f"VALIDATE: {message}")
            self.message = message

    @staticmethod
    def resolve_schema_refs(schema) -> dict:
        """Replaces the $refs within an openapi3.0 schema with the referenced components"""
        parser = ResolvingParser(spec_string=schema, backend="openapi-spec-validator")
        return parser.specification

    @classmethod
    def get_schema(cls):
        return cls._swagger_doc

    @classmethod
    def set_schema(cls, schema):
        cls._swagger_doc = schema
        cls._resolved_schema = cls.resolve_schema_refs(json.dumps(cls._swagger_doc))

    @classmethod
    def validate(cls, data, component):
        """
        Validates a request body against an component in a openapi3.0 template
        """
        if not cls._swagger_doc:
            # logging.info(f"SCHEMA: no swagger defined, loading default template")
            cls.set_schema(cls.default_swagger_template())

        components = cls._resolved_schema.get("components")
        if components is not None:
            schemas = {**components.get("schemas", {})}
            if component in schemas:
                try:
                    json_validate(instance=data, schema=schemas[component])
                except Exception as err:
                    raise cls.ValidationException(str(err))
            else:
                raise cls.ValidationException(f"SCHEMA: Does not contain {component}")

    @staticmethod
    def default_swagger_template(hostname: str = "localhost", test_mode=False) -> dict:
        # swagger doesn't understand $refs that are not relative to the doc,
        # so we replace all the canonical $refs with local markers
        def ref_update(obj):
            with suppress(KeyError):
                del obj["$id"]
            for key in obj.keys():
                if key == "$ref":
                    obj[key] = obj[key].replace("/models/", "/components/schemas/")
                    obj[key] = obj[key].replace("/definitions/", "/components/schemas/")
                    # transform global refs to local relative
                    obj[key] = obj[key].replace("http://staxapp.cloud", "#")
            return obj

        template = dict(
            openapi="3.0.0",
            info={
                "title": f"Stax Core API",
                "version": f"{os.getenv('GIT_VERSION')}",
                "description": f"The Stax API is organised around REST, uses resource-oriented URLs, return responses are JSON and uses standard HTTP response codes, authentication and verbs.",
                "termsOfService": "/there_is_no_tos",
                "contact": {"url": "https://stax.io"},
            },
            servers=[{"url": f"https://api.{hostname}"}],
            paths=dict(),
            components={
                "securitySchemes": {
                    "sigv4": {
                        "type": "apiKey",
                        "name": "Authorization",
                        "in": "header",
                        "x-amazon-apigateway-authtype": "awsSigv4",
                    }
                },
                "schemas": dict(),
                "responses": dict(),
                "requestBodies": dict(),
            },
        )
        if test_mode:
            return template

        schema_dir = os.path.dirname(os.path.realpath(__file__)) + "/.."
        for schema_type in ["models", "definitions", "responses", "requests"]:
            for schema_path in os.listdir(f"{schema_dir}/{schema_type}"):
                if not schema_path.endswith(".json"):
                    continue
                with open(
                    f"{schema_dir}/{schema_type}/{schema_path}", "rb"
                ) as schema_file:
                    # logging.debug(f"SCHEMA: loading {schema_type} {schema_path}")
                    schema = json.load(schema_file, object_hook=ref_update)
                    # logging.debug(f"SCHEMA: {schema}")
                    with suppress(KeyError):
                        del schema["$id"]
                    with suppress(KeyError):
                        del schema["$ref"]
                    with suppress(KeyError):
                        del schema["$schema"]
                    template["components"]["schemas"].update(schema)

        return template


if __name__ == "__main__":
    print(
        json.dumps(
            StaxContract.default_swagger_template(hostname="localhost"), indent=4
        )
    )

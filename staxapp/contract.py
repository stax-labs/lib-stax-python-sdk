import json
import logging
import os
import requests
from contextlib import suppress

from staxapp.exceptions import ValidationException
from staxapp.config import Config

from jsonschema import validate as json_validate
from prance import ResolvingParser

logging.getLogger("openapi_spec_validator.validators").setLevel(logging.WARNING)


class StaxContract:
    _swagger_doc = None
    _resolved_schema = None

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
                    raise ValidationException(str(err))
            else:
                raise ValidationException(f"SCHEMA: Does not contain {component}")

    @staticmethod
    def default_swagger_template() -> dict:
        # Get the default swagger template from https://api.au1.staxapp.cloud/20190206/public/api-document
        schema = requests.get(Config.schema_url()).json()
        template = dict(
            openapi="3.0.0",
            info={
                "title": f"Stax Core API",
                "version": f"{os.getenv('GIT_VERSION')}",
                "description": f"The Stax API is organised around REST, uses resource-oriented URLs, return responses are JSON and uses standard HTTP response codes, authentication and verbs.",
                "termsOfService": "/there_is_no_tos",
                "contact": {"url": "https://stax.io"},
            },
            servers=[{"url": f"https://{Config.hostname}"}],
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
                "schemas": schema,
                "responses": dict(),
                "requestBodies": dict(),
            },
        )

        return template

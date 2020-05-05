import json
import logging
import os
import uuid

import requests
from jsonschema import validate
from prance import ResolvingParser


from staxapp.api import Api
from staxapp.auth import ApiTokenAuth
from staxapp.config import ApiException, Config
from staxapp.contract import StaxContract
from staxapp.exceptions import ValidationException


class StaxClient:
    _operation_map = dict()
    _schema = dict()
    _initialized = False

    def __init__(self, classname, lambda_client=None):
        # Stax feature, eg 'quotas', 'workloads'
        self.classname = classname

        if not self._initialized:
            self._map_paths_to_operations()
            StaxContract.set_schema(self._schema)
            # logging.info(f"{self._operation_map}")
            if not self._operation_map.get(self.classname):
                raise ValidationException(
                    f"No such class: {self.classname}. Please use one of {list(self._operation_map)}"
                )
            self._initialized = True

        if lambda_client:
            self.lambda_client = lambda_client
            self._admin = True
            self.arn = f"arn:aws:lambda:{Config.api_config['Juma']['controlplaneRegion']}:{Config.api_config['Juma']['masterAccountId']}:function:{self.classname}-admninrpc-{Config.api_config['Juma']['stage']}-{Config.branch()}"
        else:
            Config.auth_class = ApiTokenAuth
            self._admin = False

    @classmethod
    def _load_schema(cls):
        if Config.load_live_schema:
            # logging.info(f"SCHEMA: loading from {Config.schema_url()}")
            schema_response = requests.get(Config.schema_url())
            schema_response.raise_for_status()
            cls._schema = schema_response.json()
        else:
            current_dir = os.path.abspath(os.path.dirname(__file__))
            schema_file = f"{current_dir}/data/schema.json"
            # logging.info(f"SCHEMA: loading from {schema_file}")
            with open(schema_file, "r") as f:
                cls._schema = json.load(f)

    @classmethod
    def _map_paths_to_operations(cls):
        cls._load_schema()
        for path_name, path in cls._schema["paths"].items():
            parameters = []
            base_path = ""
            path_parts = path_name.split("/")

            for part in path_parts:
                if "{" in part:
                    parameters.append(part.replace("{", "").replace("}", ""))
                else:
                    base_path = f"{base_path}/{part}"

            for method_type, method in path.items():
                method = path[method_type]
                operation = method.get("operationId", "").split(".")

                if len(operation) != 2:
                    continue

                api_class = operation[0]
                method_name = operation[1]

                if not cls._operation_map.get(api_class):
                    cls._operation_map[api_class] = dict()
                cls._operation_map[api_class][method_name] = dict()
                cls._operation_map[api_class][method_name]["path"] = base_path
                cls._operation_map[api_class][method_name]["method"] = method_type
                if len(parameters) > len(
                    cls._operation_map[api_class][method_name].get("parameters", [])
                ):
                    cls._operation_map[api_class][method_name][
                        "parameters"
                    ] = parameters

    def __getattr__(self, name):
        self.name = name

        def stax_wrapper(*args, **kwargs):
            method_name = f"{self.classname}.{self.name}"
            method = self._operation_map[self.classname].get(self.name)
            if method is None:
                raise ValidationException(
                    f"No such operation: {self.name} for {self.classname}. Please use one of {list(self._operation_map[self.classname])}"
                )
            payload = {**kwargs}
            parameters = ""
            preceding_parameter = False
            # All parameters starting with the most dependant
            all_schema_parameters = self._operation_map[self.classname][self.name].get(
                "parameters", []
            )
            # Get any parameters from the keyword args and remove them from the payload
            for parameter in all_schema_parameters[::-1]:
                if parameter in payload:
                    parameters = f"/{payload.pop(parameter, None)}{parameters}"
                    preceding_parameter = True
                elif preceding_parameter:
                    raise ValidationException(f"Missing parameter: {parameter}")

            if method["method"].lower() in ["put", "post"]:
                # We only validate the payload for POST/PUT routes
                StaxContract.validate(payload, method_name)
            ret = getattr(Api, method["method"])(
                f'{method["path"]}{parameters}', payload
            )
            return ret

        return stax_wrapper

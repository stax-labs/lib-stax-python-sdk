import json
import os

import requests

from staxapp.api import Api
from staxapp.auth import ApiTokenAuth
from staxapp.config import Config
from staxapp.contract import StaxContract
from staxapp.exceptions import ApiException, ValidationException


class StaxClient:
    _operation_map = dict()
    _schema = dict()
    _initialized = False

    def __init__(self, classname, lambda_client=None, force=False):
        # Stax feature, eg 'quotas', 'workloads'
        if force or not self._operation_map:
            _operation_map = dict()
            self._map_paths_to_operations()
            StaxContract.set_schema(self._schema)

        if not self._operation_map.get(classname):
            raise ValidationException(
                f"No such class: {classname}. Please use one of {list(self._operation_map)}"
            )
        self.classname = classname

        if lambda_client:
            self.lambda_client = lambda_client
            self._admin = True
            self.arn = f"arn:aws:lambda:{Config.api_config['Juma']['controlplaneRegion']}:{Config.api_config['Juma']['masterAccountId']}:function:{self.classname}-admninrpc-{Config.api_config['Juma']['stage']}-{Config.branch()}"
        else:
            Config.auth_class = ApiTokenAuth
            self._admin = False
        self._initialized = True

    @classmethod
    def _load_schema(cls):
        if Config.load_live_schema:
            schema_response = requests.get(Config.schema_url())
            schema_response.raise_for_status()
            cls._schema = schema_response.json()
        else:
            current_dir = os.path.abspath(os.path.dirname(__file__))
            schema_file = f"{current_dir}/data/schema.json"
            with open(schema_file, "r") as f:
                cls._schema = json.load(f)

    @classmethod
    def _map_paths_to_operations(cls):
        cls._load_schema()
        for path_name, path in cls._schema["paths"].items():
            parameters = []

            for part in path_name.split("/"):
                if "{" in part:
                    parameters.append(part.replace("{", "").replace("}", ""))

            for method_type, method in path.items():
                method = path[method_type]
                operation = method.get("operationId", "").split(".")

                if len(operation) != 2:
                    continue

                parameter_path = {
                    "path": path_name,
                    "method": method_type,
                    "parameters": parameters,
                }

                api_class = operation[0]
                method_name = operation[1]
                if not cls._operation_map.get(api_class):
                    cls._operation_map[api_class] = dict()
                if not cls._operation_map.get(api_class, {}).get(method_name):
                    cls._operation_map[api_class][method_name] = []

                cls._operation_map[api_class][method_name].append(parameter_path)

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

            sorted_parameter_paths = sorted(
                self._operation_map[self.classname][self.name],
                key=lambda x: len(x["parameters"]),
            )
            # All parameters starting with the most dependant
            operation_parameters = [
                parameter_path["parameters"]
                for parameter_path in sorted_parameter_paths
            ]
            # Sort the operation map parameters
            parameter_index = -1
            # Check if the any of the parameter schemas match parameters provided
            for index in range(0, len(operation_parameters)):
                # Get any parameters from the keyword args and remove them from the payload
                if set(operation_parameters[index]).issubset(payload.keys()):
                    parameter_index = index
            if parameter_index == -1:
                raise ValidationException(
                    f"Missing one or more parameters: {operation_parameters[-1]}"
                )
            paramter_path = sorted_parameter_paths[parameter_index]
            split_path = paramter_path["path"].split("/")
            path = ""
            for part in split_path:
                if "{" in part:
                    parameter = part.replace("{", "").replace("}", "")
                    path = f"{path}/{payload.pop(parameter)}"
                else:
                    path = f"{path}/{part}"
            if paramter_path["method"].lower() in ["put", "post"]:
                # We only validate the payload for POST/PUT routes
                StaxContract.validate(payload, method_name)
            ret = getattr(Api, paramter_path["method"])(path, payload)
            return ret

        return stax_wrapper

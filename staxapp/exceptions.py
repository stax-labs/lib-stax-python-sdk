import logging
from json.decoder import JSONDecodeError


class ApiException(Exception):
    def __init__(self, message, response, detail=""):
        try:
            self.status_code = response.status_code
            if response.json().get("Error"):
                logging.error(f"{response.status_code}: {response.json()}")
                self.message = f"Api Exception: {response.status_code} -{detail} {response.json()['Error']}"
            else:
                logging.error(f"{response.status_code}: {response.json()}")
                self.message = f"Api Exception:{detail} {message}"
        except:
            if response.content:
                logging.error(f"{response.status_code}: {response.content}")
            else:
                logging.error(f"{response.status_code}: {message}")
            self.message = f"Api Exception:{detail} {message}"

    def __str__(self):
        return self.message


class ValidationException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidCredentialsException(Exception):
    def __init__(self, message, detail=""):
        logging.error(message)
        prefix = f"InvalidCredentialsException: "
        if detail:
            prefix = f"{prefix}{detail} - "
        self.message = f"{prefix}{message}"

    def __str__(self):
        return self.message

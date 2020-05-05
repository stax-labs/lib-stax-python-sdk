class ApiException(Exception):
    def __init__(self, message, response, detail=""):
        prefix = f"Api Exception: {response.status_code} - "
        if detail:
            prefix = f"{prefix}{detail} "
        if response.json().get("Error"):
            print("Some error")
            self.message = f"{prefix}{response.json()['Error']}"
        else:
            print("No Error")
            self.message = f"{prefix}{message}"

    def __str__(self):
        return self.message


class ValidationException(Exception):
    def __init__(self, message):
        # logging.info(f"VALIDATE: {message}")
        self.message = message

import os

from staxapp.config import Config
from staxapp.openapi import StaxClient
from staxapp.exceptions import InvalidCredentialsException

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all workload catalogue items within your Stax Organisation
try:
	workloads = StaxClient("workloads")
except InvalidCredentialsException as e:
	print(e)
	# Try other credentials

import os

from staxapp.config import Config
from staxapp.openapi import StaxClient
from staxapp.exceptions import ApiException

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all workload catalogue items within your Stax Organisation
workloads = StaxClient("workloads")
try:
	response = workloads.ReadCatalogueItems()
except ApiException as e:
	print(e)
	if e.status_code == 404:
		print("No Catalogues exist")

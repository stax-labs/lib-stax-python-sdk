import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

response = networks.DeleteDnsResolver(dns_resolver_id="<resolver_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))

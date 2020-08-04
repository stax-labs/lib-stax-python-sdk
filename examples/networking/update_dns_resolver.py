import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

body = {
    "Name": "my-testing-resolver-2",
    "NumberOfInterfaces": 3
}
response = networks.UpdateDnsResolver(dns_resolver_id="<resolver_uuid>", **body)

print(response.json())
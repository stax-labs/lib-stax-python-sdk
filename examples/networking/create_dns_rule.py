import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API Schema for valid body properties

networks = StaxClient("networking")

# create a DNS Rule within a Stax DNS Resolver by providing the `dns_resolver_uuid` and body properties

body = {
    "DomainName": "test.local",
    "ForwarderIpAddresses": [
        "192.168.0.1",
        "192.168.0.2"
    ],
    "Name": "on-premises",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.CreateDnsRule(dns_resolver_id="<dns_resolver_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))

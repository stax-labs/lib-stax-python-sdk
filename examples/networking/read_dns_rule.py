import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# if `status` filter is not provided, only resources with the following statuses will be returned by default: ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,UPDATE_IN_PROGRESS

networks = StaxClient("networking")

# read all DNS Rules within the Organization
response = networks.ReadDnsResolvers()

# query all DNS Rules within the Organization, filtered by status
response = networks.ReadDnsResolvers(status="ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,DELETE_IN_PROGRESS,DELETED,DELETE_FAILED,UPDATE_IN_PROGRESS")

# read the details of a DNS Rule by providing by providing a `dns_resolver_id
response = networks.ReadDnsResolvers(dns_resolver_id="<resolver_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))

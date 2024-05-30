import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient
from customscript import get_hostnames
hostname = get_hostnames()

access_key = os.getenv("STAX_ACCESS_KEY")
secret_key = os.getenv("STAX_SECRET_KEY")

Config.hostname = hostname["au1"]
Config.access_key = access_key
Config.secret_key = secret_key

accounts_au1 = StaxClient('accounts')

au1_response = accounts_au1.CreateAccountType(
    Name="sdk-au1"
)

print(json.dumps(au1_response, indent=4, sort_keys=True))

access_key_2 = os.getenv("STAX_ACCESS_KEY_2")
secret_key_2 = os.getenv("STAX_SECRET_KEY_2")
config = Config(hostname=hostname["us1"], access_key=access_key_2, secret_key=secret_key_2)

us1_accounts = StaxClient('accounts', config=config)

us1_response = us1_accounts.CreateAccountType(
    Name="sdk-us1"
)
print(json.dumps(us1_response, indent=4, sort_keys=True))

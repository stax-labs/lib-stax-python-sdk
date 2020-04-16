import os
import json

from stax.config import Config
from stax.openapi import StaxClient

Config.access_key = os.getenv("TEST_ACCESS_KEY")
Config.secret_key = os.getenv("TEST_SECRET_KEY")

client = StaxClient("accounts")
client.CreateAccount(
    Name="bad-tags-test-001", 
    Tags=json.dumps({"Not": "Really", "Tags": "Insteads", "Its": "String"}),
)

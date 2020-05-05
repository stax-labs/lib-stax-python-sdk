# Stax SDK for Python
`staxapp` is the [Stax](https://stax.io) Software Development Kit (SDK) for Python, allowing users to interact with the Stax platform.

![Build](https://github.com/stax-labs/lib-stax-python-sdk/workflows/Build/badge.svg)

## Authentication
In order to use the Stax SDK for Python, you will need a valid [Stax API Token](https://www.stax.io/docs/stax_team/access_stax_api_with_an_api_token/).

## Installation
Install the package using `pip`:
```bash
pip install staxapp
```
Configure environment variables:

```bash
export STAX_REGION=au1.staxapp.cloud
export STAX_ACCESS_KEY=<your_access_key>
export STAX_SECRET_KEY=<your_secret_key>
```

## Code Examples

### Read Accounts
The following code can be used to read accounts within your Stax Organisation:
```python
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all accounts within your Stax Organisation
accounts = StaxClient("accounts")
response = accounts.ReadAccounts()
print(response)

# Read all active accounts within your Stax Organisation and include tags in the response
accounts = StaxClient("accounts")
response = accounts.ReadAccounts(filter="ACTIVE", include_tags=True)
print(response)
```


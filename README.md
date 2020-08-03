# Stax SDK for Python
`staxapp` is the [Stax](https://stax.io) Software Development Kit (SDK) for Python, allowing users to interact with the Stax platform.

[![codecov](https://codecov.io/gh/stax-labs/lib-stax-python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/stax-labs/lib-stax-python-sdk)
![build](https://github.com/stax-labs/lib-stax-python-sdk/workflows/build/badge.svg)
![deploy](https://github.com/stax-labs/lib-stax-python-sdk/workflows/deploy/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/staxapp)
## Authentication
In order to use the Stax SDK for Python, you will need a valid [Stax API Token](https://www.stax.io/developer/api-tokens/).

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

## Usage

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
print(response.json())

# Read all active accounts within your Stax Organisation and include tags in the response
accounts = StaxClient("accounts")
response = accounts.ReadAccounts(filter="ACTIVE", include_tags=True)
print(response.json())
```

## Contributing
For more information on contributing the to the Stax SDK, please see our [guide](https://github.com/stax-labs/lib-stax-python-sdk/blob/master/CONTRIBUTING.md).

## Getting Help
* If you're having trouble using the Stax SDK, please refer to our [documentation](https://www.stax.io/developer/api-tokens/).<br>
* If you've encountered an issue or found a bug, please [open an issue](https://github.com/stax-labs/lib-stax-python-sdk/issues).<br>
* For any other requests, please contact [Stax support](mailto:support@stax.io).
 

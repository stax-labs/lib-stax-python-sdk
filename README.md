[Python - Logging Levels]:https://docs.python.org/3/library/logging.html#levels
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

##### Client Auth Configuration
You can configure each client individually by passing in a config on init.
When a client is created it's configuration will be locked in and any change to the configurations will not affect the client.

This can be seen in our [guide](https://github.com/stax-labs/lib-stax-python-sdk/blob/master/examples/auth.py).

*Optional configuration:*

##### Authentication retries and token expiry

Allows configuration of the maximum number of attempts and the threshold to when the Auth library should re-cache the credentials
*Suggested use when running within CI/CD tools to reduce overall auth calls*
~~~bash
export STAX_API_AUTH_MAX_RETRIES=5
export TOKEN_EXPIRY_THRESHOLD_IN_MINS=2 # Type: Integer representing minutes
~~~

##### Logging levels

As the logging levels are set on the import of the `Config` module, the below configuration is available on the presense of following environment variables:

- LOG_LEVEL: Default logger level

Value of environment variables should match [Python - Logging Levels]

Example:
Changing the logging from `INFO` to `DEBUG`
~~~bash
export LOG_LEVEL=DEBUG
python run_example.py
~~~

## Usage

### Read Accounts
The following code can be used to read accounts within your Stax Organisation:
```python
import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all accounts within your Stax Organisation
accounts = StaxClient("accounts")
response = accounts.ReadAccounts()
print(json.dumps(response, indent=4, sort_keys=True))

# Read all active accounts within your Stax Organisation and include tags in the response
accounts = StaxClient("accounts")
response = accounts.ReadAccounts(filter="ACTIVE", include_tags=True)
print(json.dumps(response, indent=4, sort_keys=True))
```

## Contributing
For more information on contributing the to the Stax SDK, please see our [guide](https://github.com/stax-labs/lib-stax-python-sdk/blob/master/CONTRIBUTING.md).

## Getting Help
* If you're having trouble using the Stax SDK, please refer to our [documentation](https://www.stax.io/developer/api-tokens/).<br>
* If you've encountered an issue or found a bug, please [open an issue](https://github.com/stax-labs/lib-stax-python-sdk/issues).<br>
* For any other requests, please contact [Stax support](mailto:support@stax.io).


## Install
```bash
pip install stax
```

## Configuration

```bash
export AWS_DEFAULT_REGION=ap-southeast-2
export STAX_REGION=au1.staxapp.cloud
```

## Examples

### Create or update a Workload Catalogue
```python
from stax.config import Config
from stax.openapi import StaxClient

Config.access_key = 'walter@lebowski.org'
Config.secret_key = '<very secret>'

manifest_body = ""
with open('IDAM-workload.out.yml', 'r') as manifest:
    manifest_body = manifest.read()

payload = {
}
client = StaxClient("workloads")
client.CreateCatalogueItem(
    Name="stax-example",
    ManifestBody=manifest_body,
    Version="4.8.3",
    Description="stax-example workload",
)
```

### Get an AWS Account Id
```python
from stax.config import Config
from stax.openapi import StaxClient

Config.access_key = 'donny@lebowski.org'
Config.secret_key = '<very secret>'

accounts = StaxClient("accounts")
account = [account for account in accounts.ReadAccounts()["Accounts"] if account["Name"] == "logging"][0]
print(account["AwsAccountId"])
```

### Arbitrary API request
```python
from stax.config import Config
from stax.openapi import StaxClient

Config.access_key = 'thebig@lebowski.org'
Config.secret_key = '<very secret>'

client = StaxClient("accounts")
response = client.ReadAccounts()
print(response)
```

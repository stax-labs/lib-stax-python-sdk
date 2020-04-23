How to get Api_Tokens
There are 2 things you'll need to know how to do
- How to log in to the awscli (eg using saml2aws and using you personal access token)
- How to make an api request (eg using postman)
There are 3 names you'll need to know or create for this tutorial
- The account/s that will access your api tokens (the aws id)
- The api-token's name (only include +=,.@_- in the name or alpha-numeric) that will be created
- The deployment bucket name that you use to create workloads from

1. Create an account/use a customer account (postman / ui)
2. Use saml2aws to log in to your account
3. Deploy the stax-deployment-bucket (you can find your org id by logging into you account and finding the aws org) (postman/ui)
4. Use the api to generate an api token  (postman)
5. Use the name to run upload_api_token_cfn.py
6. Take the deployment bucket full name (the output of upload_api_token_cfn.py) and insert it into api_token_workload.yaml
5. Create a workload-catalogue and upload api_token_workload.yaml (postman/ui)
6. Deploy the workload catalogue into the security account using the account and the api token name as parameters
7. Run the get creds scripts (saml2aws)

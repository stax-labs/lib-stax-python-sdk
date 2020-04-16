from setuptools import setup, find_packages

requires = ["boto3", "prance", "requests", "aws_requests_auth", "warrant", "pycrypto", "pyjwt", "openapi-spec-validator"]

setup(
    name="stax",
    version="0.4",
    description="Stax Python SDK",
    url="https://github.com/stax-labs/lib-stax-python-sdk",
    author="Stax",
    author_email="support@stax.io",
    license="MIT",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=requires,
    include_package_data=True,
    package_data={"stax": ["data/*.json"]},
    zip_safe=False,
)

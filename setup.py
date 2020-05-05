from setuptools import setup, find_packages
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requires = ["boto3", "prance", "requests", "aws_requests_auth", "warrant", "pycrypto", "pyjwt", "openapi-spec-validator"]

setup(
    name="staxapp",
    version="0.4",
    description="Stax Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stax.io",
    author="Stax",
    author_email="support@stax.io",
    license="Apache Software License",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=requires,
    include_package_data=True,
    package_data={"staxapp": ["data/*.json"]},
    zip_safe=False,
    python_requires='>=3',
    project_urls={
        "GitHub": "https://github.com/stax-labs/lib-stax-python-sdk"
    },
)

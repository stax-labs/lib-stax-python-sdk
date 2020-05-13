from setuptools import setup, find_packages
import os
import re

requires = [
    "boto3",
    "prance",
    "requests",
    "aws_requests_auth",
    "warrant",
    "pycrypto",
    "pyjwt",
    "openapi-spec-validator",
]


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")


def get_version():
    init = open(os.path.join(ROOT, "staxapp", "__init__.py")).read()
    return VERSION_RE.search(init).group(1)


setup(
    name="staxapp",
    version=get_version(),
    description="Stax Python SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://stax.io",
    author="Stax",
    author_email="support@stax.io",
    license="Apache License 2.0",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=requires,
    include_package_data=True,
    package_data={"staxapp": ["data/*.json"]},
    zip_safe=False,
    python_requires=">=3.6",
    project_urls={"GitHub": "https://github.com/stax-labs/lib-stax-python-sdk"},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

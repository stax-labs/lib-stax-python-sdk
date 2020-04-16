# vim:set noexpandtab :
.PHONY: help test install lint format

export AWS_PROFILE
export AWS_DEFAULT_REGION

CURRENT_DIRECTORY=$(shell pwd)
VIRTUAL_ENV?=$(CURRENT_DIRECTORY)/venv
PIP?=${VIRTUAL_ENV}/bin/pip
PYTHON?=${VIRTUAL_ENV}/bin/python
BLACK?=${VIRTUAL_ENV}/bin/black
ISORT?=${VIRTUAL_ENV}/bin/isort
NOSE?=${VIRTUAL_ENV}/bin/nose2


.DEFAULT: help
help:
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run black"

test:
	${NOSE}

install:
	python3 -m venv ${VIRTUAL_ENV}
	${PIP} install -r requirements.txt

lint: install
	${ISORT} --diff stax/*.py
	${BLACK} -t py37 --diff stax/

format: lint
	${ISORT} --apply stax/*.py
	${BLACK} -t py37 stax/

download-schema:
	curl --fail --compressed -s -o stax/data/schema.json https://api.au1.staxapp.cloud/20190206/public/api-document

bundle-test: install
	${PIP} install twine
	${PYTHON} setup.py sdist
	${VIRTUAL_ENV}/bin/twine check dist/*
	${VIRTUAL_ENV}/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

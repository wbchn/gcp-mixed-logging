# Make will use bash instead of sh
SHELL := /usr/bin/env bash

ROOT := ${CURDIR}
GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: test
test:
	GCLOUD_PROJECT=$(GCLOUD_PROJECT) python3 setup.py test

.PHONY: clean
clean:
	@rm -fr build dist .eggs *.egg-info
	@rm -fr */__pycache__
	gcloud beta logging logs delete data_test --project $(GCLOUD_PROJECT) --quiet

.PHONY: package
package:
	@rm -fr build dist .eggs *.egg-info
	python3 setup.py sdist bdist_wheel

.PHONY: dist
dist:
	python3 -m twine check dist/*
	python3 -m twine upload dist/*
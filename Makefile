# Make will use bash instead of sh
SHELL := /usr/bin/env bash

ROOT := ${CURDIR}
GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: test
test:
	GCLOUD_PROJECT=$(GCLOUD_PROJECT) python3 setup.py test

.PHONY: clean
clean:
	gcloud beta logging logs delete data_test --project $(GCLOUD_PROJECT) --quiet

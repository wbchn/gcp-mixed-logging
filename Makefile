# Make will use bash instead of sh
SHELL := /usr/bin/env bash

ROOT := ${CURDIR}
GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: test
test:
	GCLOUD_PROJECT=$(GCLOUD_PROJECT) pytest

.PHONY: clean
clean:
	gcloud beta logging logs delete data_test_stdout --project $(GCLOUD_PROJECT) --quiet
	gcloud beta logging logs delete data_test_stderr --project $(GCLOUD_PROJECT) --quiet

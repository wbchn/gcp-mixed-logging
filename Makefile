# Make will use bash instead of sh
SHELL := /usr/bin/env bash

ROOT := ${CURDIR}
GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: test
test:
	pytest

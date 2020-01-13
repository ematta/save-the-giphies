SHELL = /bin/bash


.PHONY: run-api
run-api:
	cd server && $(MAKE) install check-code debug

.PHONY: run-ui
run-ui:
	cd client && $(MAKE) run

.PHONY: pipeline
pipeline:
	cd server && $(MAKE) install check-code unit-test integration-test
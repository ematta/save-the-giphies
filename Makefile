SHELL = /bin/bash


.PHONY: run-api
run-api:
	cd server && $(MAKE) install check-code all

.PHONY: run-ui
run-ui:
	cd client && npm i && npm run serve
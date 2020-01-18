SHELL = /bin/bash
.DEFAULT_GOAL := all

.PHONY: all
all: fix
	@npm run serve

.PHONY: fix
fix:
	@npm run lint -- --fix

.PHONY: pipeline
pipeline:
	@npm run lint \
	&& npm run build;
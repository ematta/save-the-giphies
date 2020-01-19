SHELL = /bin/bash
.DEFAULT_GOAL := all

.PHONY: all
all: install
	@. .venv/bin/activate; \
	DEBUG=True python app.py

.PHONY: check-code
check-code: install mypy black flake8 static packages

.PHONY: mypy
mypy:
	@. .venv/bin/activate; \
	mypy save_the_giphies;

.PHONY: black
black:
	@. .venv/bin/activate; \
	black save_the_giphies --exclude .venv; \

.PHONY: flake8
flake8:
	@. .venv/bin/activate; \
	flake8 save_the_giphies --exclude .venv -v;

.PHONY: check-tests
check-tests: 
	@. .venv/bin/activate; \
	mypy tests; \
	black tests --exclude .venv; \
	flake8 tests --exclude .venv

.PHONY: destroy
destroy:
	@. .venv/bin/activate; \
	pip freeze | xargs pip uninstall -y

.PHONY: install
install: venv
	@. .venv/bin/activate \
	&& pip install --upgrade pip \
	&& pip install -r requirements.txt -r dev-requirements.txt;
	
.PHONY: venv
venv:
	@if [ ! -d .venv ]; then \
		python3 -m venv .venv; \
	fi

.PHONY: functional-test
functional-test:
	@. .venv/bin/activate; \
	python -m unittest discover tests/functional -v

.PHONY: integration-test
integration-test: report
	@. .venv/bin/activate; \
	coverage run -m unittest discover tests/integration -v

.PHONY: unit-test
unit-test: report
	@. .venv/bin/activate; \
	coverage run -m unittest discover tests/unit -v

.PHONY: report
report:
	@. .venv/bin/activate; \
	coverage html

.PHONY: tests
tests: check-tests unit-test integration-test functional-test

.PHONY: pipeline
pipeline: 
	pip install --upgrade pip \
	&& pip install -r pipeline-requirements.txt -r dev-requirements.txt \
	&& mypy save_the_giphies \
	&& black save_the_giphies --exclude .venv \
	&& flake8 save_the_giphies --exclude .venv \
	&& python -m unittest discover tests/integration -v \
	&& python -m unittest discover tests/unit -v;

.PHONY: packages
packages:
	@. .venv/bin/activate; \
	safety check -r requirements.txt;

.PHONY: static
static:
	# Skipping B310 because this is an external call and complains
	# about the schema not being there (in config)
	@. .venv/bin/activate; \
	bandit -r -s B310 save_the_giphies
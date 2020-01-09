SHELL = /bin/bash


.PHONY: check-code
check-code: 
	@. .venv/bin/activate; \
	mypy save_the_giphies; \
	black save_the_giphies --exclude .venv; \
	flake8 save_the_giphies --exclude .venv

.PHONY: check-tests
check-tests: 
	@. .venv/bin/activate; \
	mypy test; \
	black test --exclude .venv; \
	flake8 test --exclude .venv

.PHONY: destroy
destroy:
	@. .venv/bin/activate; pip freeze | xargs pip uninstall -y

.PHONY: install
install: venv
	@. .venv/bin/activate \
	&& pip install --upgrade pip \
	&& pip install -r requirements.txt;
	
.PHONY: venv
venv:
	@if [ ! -d .venv ]; then \
		python3 -m venv .venv; \
	fi

.PHONY: functional-test
functional-test:
	@. .venv/bin/activate; python -m unittest discover test/functional -v

.PHONY: integration-test
integration-test:
	@. .venv/bin/activate; python -m unittest discover test/integration -v

.PHONY: unit-test
unit-test:
	@. .venv/bin/activate; python -m unittest discover test/unit -v

.PHONY: tests
tests: check-tests unit-test integration-test functional-test
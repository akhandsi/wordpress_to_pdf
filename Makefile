# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=20
## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

## Clean all files
clean:
	rm -rf venv
	rm -rf dist
	rm -rf build
	rm -rf scripts/__pycache__
	rm -rf *.egg-info
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "*.pyo" -exec rm -rf {} \;

## install application
install: _initvenv _development
	. venv/bin/activate

_initvenv: clean
	python3 -m virtualenv venv

_development:
	venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install --upgrade setuptools
	venv/bin/pip3 install progressbar2
	venv/bin/pip3 install -Ur requirements.txt
	venv/bin/pip3 install --editable .

.PHONY: help clean install

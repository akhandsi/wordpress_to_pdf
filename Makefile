.PHONY: help
help : Makefile
	python scripts/start.py --help

.PHONY: install
install:
	pip install -r requirements.txt
	pip install --editable .
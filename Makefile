.PHONY: lint format run setup clean

SHELL := /bin/bash

ifeq ($(OS),Windows_NT)
    VENV_PYTHON := venv\Scripts\python.exe
else
    VENV_PYTHON := venv/bin/python
endif

PYTHON := python

run:
	$(VENV_PYTHON) run.py

lint:
	$(VENV_PYTHON) -m ruff check . --fix

format:
	$(VENV_PYTHON) -m ruff format .

setup:
	$(PYTHON) -m venv venv
	$(VENV_PYTHON) -m pip install -r requirements.txt

clean:
	rm -rf venv
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

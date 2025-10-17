# Makefile for fastinit development

.PHONY: install dev-install test lint format type-check clean build publish help

help:
	@echo "fastinit Development Commands"
	@echo "=============================="
	@echo "install       - Install package in normal mode"
	@echo "dev-install   - Install package in development mode with dev dependencies"
	@echo "test          - Run tests"
	@echo "lint          - Run linter"
	@echo "format        - Format code with black"
	@echo "type-check    - Run type checker"
	@echo "clean         - Clean build artifacts"
	@echo "build         - Build package"
	@echo "publish       - Publish to PyPI"

install:
	pip install .

dev-install:
	pip install -e .
	pip install pytest black flake8 mypy twine build

test:
	pytest -v

lint:
	flake8 fastinit/ --max-line-length=100 --exclude=__pycache__,.git,venv,env

format:
	black fastinit/ tests/ --line-length=100

type-check:
	mypy fastinit/ --ignore-missing-imports

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

example-basic:
	fastinit init example-basic --force

example-full:
	fastinit init example-full --db --jwt --logging --docker --force

example-crud:
	cd example-full && fastinit new crud Product --fields "name:str,price:float,description:text"

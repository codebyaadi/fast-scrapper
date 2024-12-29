# Variables
APP_NAME := app.main:app
PYTHON := python
UVICORN := uvicorn
BLACK := black

# Default target
.PHONY: help
help:
	@echo "Makefile for FastAPI project"
	@echo "Usage:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run code linters"
	@echo "  make format      - Run code formatter"
	@echo "  make clean       - Clean temporary files"
	@echo "  make build       - Build the project (optional)"
	@echo "  make run         - Run the project directly"
	@echo "  make freeze      - Freeze current dependencies into requirements.txt"

# Install dependencies
.PHONY: install
install:
	@pip install -r requirements.txt

# Run development server
.PHONY: dev
dev:
	$(UVICORN) $(APP_NAME) --reload

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest

# Lint code
.PHONY: lint
lint:
	$(PYTHON) -m flake8 app tests

# Format code with Black
.PHONY: format
format:
	$(BLACK) .

# Clean up temporary files
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.pytest_cache" -exec rm -r {} +

# Build the project (optional, for packaging)
.PHONY: build
build:
	@python setup.py sdist bdist_wheel

# Run the project directly
.PHONY: run
run:
	$(PYTHON) -m $(APP_NAME)

# Freeze current environment dependencies into requirements.txt
.PHONY: freeze
freeze:
	@pip freeze > requirements.txt

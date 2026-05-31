.PHONY: install install-dev test lint format clean build upload help

help:
	@echo "CodeSnap CLI - Available commands:"
	@echo "  make install      - Install the package"
	@echo "  make install-dev  - Install in development mode with dev dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make upload       - Upload to PyPI"
	@echo "  make run          - Run the CLI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=codesnap --cov-report=term-missing

lint:
	flake8 codesnap/ tests/
	pylint codesnap/
	mypy codesnap/

format:
	black codesnap/ tests/
	isort codesnap/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine check dist/*
	twine upload dist/*

run:
	python -m codesnap.cli

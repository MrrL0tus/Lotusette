.PHONY: help install install-dev test lint format clean run

help:
	@echo "Lotusette - Makefile commands"
	@echo ""
	@echo "install          Install production dependencies"
	@echo "install-dev      Install development dependencies"
	@echo "test             Run tests with coverage"
	@echo "lint             Run linters (flake8, pylint, mypy)"
	@echo "format           Format code with black and isort"
	@echo "clean            Remove build artifacts and caches"
	@echo "run              Run the CLI interface"
	@echo "api              Run the API server"
	@echo "docker-build     Build Docker image"
	@echo "docker-up        Start Docker compose services"
	@echo "docker-down      Stop Docker compose services"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest

test-verbose:
	pytest -v -s

coverage:
	pytest --cov=lotusette --cov-report=html --cov-report=term

lint:
	flake8 lotusette tests
	pylint lotusette
	mypy lotusette

format:
	black lotusette tests
	isort lotusette tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .pytest_cache .coverage htmlcov .mypy_cache

run:
	python -m lotusette.cli

api:
	uvicorn lotusette.api.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t lotusette:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

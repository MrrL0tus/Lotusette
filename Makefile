.PHONY: help install install-dev test lint typecheck format clean run

help:
	@echo "Lotusette - Makefile commands"
	@echo ""
	@echo "install          Install production dependencies"
	@echo "install-dev      Install development dependencies"
	@echo "test             Run the test suite"
	@echo "coverage         Run tests with a coverage report"
	@echo "lint             Run ruff (blocking)"
	@echo "typecheck        Run mypy (advisory)"
	@echo "format           Format and auto-fix code with ruff"
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

test:
	pytest

test-verbose:
	pytest -v -s

coverage:
	pytest --cov=lotusette --cov-report=html --cov-report=term

# Bloquant : doit rester vert.
lint:
	ruff check lotusette tests examples
	ruff format --check lotusette tests examples

# Indicatif : ~33 erreurs préexistantes, essentiellement des types SQLAlchemy
# et des **kwargs vers les SDK. À résorber progressivement, pas bloquant.
typecheck:
	-mypy lotusette

format:
	ruff format lotusette tests examples
	ruff check --fix lotusette tests examples

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .pytest_cache .coverage htmlcov .mypy_cache

run:
	python -m lotusette.ui.cli

api:
	uvicorn lotusette.api.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t lotusette:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

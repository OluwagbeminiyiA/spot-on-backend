.PHONY: all clean run-server migrate create-superuser migrations install shell test test_api

all: install migrations migrate
	@echo "Setup complete! Run 'make run-server' to start the development server."

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

run-server:
	poetry run python -m core_spoton.manage runserver

migrate:
	poetry run python -m core_spoton.manage migrate

create-superuser:
	poetry run python -m core_spoton.manage createsuperuser

migrations:
	poetry run python -m core_spoton.manage makemigrations

install:
	poetry install

shell:
	poetry run python -m core_spoton.manage shell

test:
	poetry run python -m core_spoton.manage test

test_api:
	poetry run python -m core_spoton.manage test core_spoton.api

install-pre-commit:
	poetry run pre-commit clean
	poetry run pre-commit install

lint:
	poetry run pre-commit run --all-files

update:
	poetry run pre-commit autoupdate

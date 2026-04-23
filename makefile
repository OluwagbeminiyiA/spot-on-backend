.PHONY: run-server
run-server:
	poetry run python -m core_spoton.manage runserver


.PHONY: migrate
migrate:
	poetry run python -m core_spoton.manage migrate


.PHONY: create-superuser
create-superuser:
	poetry run python -m core_spoton.manage createsuperuser

.PHONY: migrations
migrations:
	poetry run python -m core_spoton.manage makemigrations

.PHONY: install
install:
	poetry install

.PHONY: shell
shell:
	poetry run python -m core_spoton.manage shell


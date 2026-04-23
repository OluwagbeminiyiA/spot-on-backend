.PHONY: run-server
run-server:
	poetry run python -m core_spoton.manage runserver


.PHONY: migrate
migrate:
	poetry run python manage.py migrate


.PHONY: create-superuser
create-superuser:
	poetry run python manage.py createsuperuser

.PHONY: migrations
migrations:
	poetry run python manage.py makemigrations

.PHONY: install
install:
	poetry install



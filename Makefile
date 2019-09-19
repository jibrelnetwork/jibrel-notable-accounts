shell:
	docker-compose run --rm dev sh

build:
	@docker-compose build

mypy:
	@docker-compose run --rm dev mypy .

lint:
	@docker-compose run --rm dev flake8 .

test:
	@docker-compose run --rm dev pytest .

validate:
	make lint
	make mypy
	make test

migrations:
	@docker-compose run --rm dev alembic revision -m "$(m)"

migrate:
	@docker-compose run --rm dev alembic upgrade head

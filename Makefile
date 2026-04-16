run:
	docker compose up --build

test:
	docker compose run --rm web python manage.py test

migrate:
	docker compose run --rm web python manage.py migrate

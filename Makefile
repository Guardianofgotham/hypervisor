migrate:
	docker compose --env-file .env run web python manage.py migrate

makemigrations:
	docker compose --env-file .env run web python manage.py makemigrations
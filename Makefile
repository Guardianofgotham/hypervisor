migrate:
	docker compose --env-file .env run web python manage.py migrate

makemigrations:
	docker compose --env-file .env run web python manage.py makemigrations

shell:
	docker compose --env-file .env run web python manage.py shell

test:
	docker compose --env-file .env run web python manage.py test

clean:
	docker compose down
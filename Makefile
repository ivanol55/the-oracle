.PHONY: up down build logs

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart: down up

populate:
	POPULATE_CHROMA=True docker compose up -d api_backend

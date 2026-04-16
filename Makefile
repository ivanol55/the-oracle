.PHONY: up down build logs restart sync-logs

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

sync-logs:
	docker compose logs -f data_sync

restart: down up

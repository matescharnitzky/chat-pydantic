.PHONY: install check up down test-api

install:
	uv sync --all-packages --all-groups

check:
	uv run ruff format --check .
	uv run ruff check .
	LOGFIRE_SEND_TO_LOGFIRE=false uv run pytest -q

up:
	docker compose up --build --wait

down:
	docker compose down

test-api:
	cd bruno && bru run --env local

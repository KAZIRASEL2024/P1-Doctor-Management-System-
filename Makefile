# BRAC AISP Doctor Management System — Makefile
# Requires Docker and Docker Compose.
# On Windows, use `nmake` or run the equivalent scripts\ PowerShell files.

.PHONY: up down reset build logs test migrate seed shell-backend shell-db

COMPOSE = docker compose -f docker-compose.yml -f docker-compose.dev.yml

up:
	@echo "Starting development stack..."
	$(COMPOSE) up -d
	@echo "Frontend  : http://localhost:3000"
	@echo "Backend   : http://localhost:8000/api/docs"

down:
	$(COMPOSE) down

reset:
	$(COMPOSE) down -v
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f

logs-backend:
	$(COMPOSE) logs -f backend

test:
	$(COMPOSE) run --rm backend sh -c \
		"pip install aiosqlite --quiet && pytest tests/ -v --tb=short"

migrate:
	$(COMPOSE) exec backend alembic upgrade head

seed:
	$(COMPOSE) exec backend python -m scripts.seed_demo_data

shell-backend:
	$(COMPOSE) exec backend bash

shell-db:
	$(COMPOSE) exec db psql -U dms_user -d doctor_management

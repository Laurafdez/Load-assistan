# -------------------------------
# Metadata
# -------------------------------
VERSION_MAJOR ?= 1
VERSION_MINOR ?= 0
VERSION_PATCH ?= 0
VERSION ?= $(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_PATCH)

PORT ?= 8000
HOST ?= 127.0.0.1
ENV_FILE ?= .env
DC_FILE ?= docker-compose.yml

# -------------------------------
# Dependencies
# -------------------------------
.PHONY: install
install:
	poetry install

.PHONY: update
update:
	poetry update

# -------------------------------
# Code Quality
# -------------------------------
.PHONY: lint
lint:
	poetry run ruff check app tests

.PHONY: lint-fix
lint-fix:
	poetry run ruff check app tests --fix

.PHONY: quality
quality: lint test

# -------------------------------
# Testing
# -------------------------------
.PHONY: test
test:
	poetry run pytest

.PHONY: coverage
coverage:
	poetry run pytest --cov=app --cov-report=term-missing

# -------------------------------
# Run App
# -------------------------------
.PHONY: run
run:
	poetry run uvicorn app.main:app --reload --host $(HOST) --port $(PORT)

.PHONY: serve
serve: run

.PHONY: run-ngrok
run-ngrok:
	poetry run uvicorn app.main:app --reload --port $(PORT) &
	sleep 2
	ngrok http $(PORT)

# -------------------------------
# Docker
# -------------------------------
.PHONY: docker-build
docker-build:
	docker build -t load-agent-api .

.PHONY: docker-run
docker-run:
	docker run --env-file $(ENV_FILE) -p $(PORT):$(PORT) load-agent-api

.PHONY: docker-clean
docker-clean:
	docker container prune --force

# -------------------------------
# Docker Compose
# -------------------------------
.PHONY: dc-up
dc-up:
	docker compose -f $(DC_FILE) up -d

.PHONY: dc-down
dc-down:
	docker compose -f $(DC_FILE) down

.PHONY: dc-build
dc-build:
	docker compose -f $(DC_FILE) build

.PHONY: dc-logs
dc-logs:
	docker compose -f $(DC_FILE) logs -f

.PHONY: dc-restart
dc-restart:
	docker compose -f $(DC_FILE) down && docker compose -f $(DC_FILE) up -d --build

.PHONY: dc-shell
dc-shell:
	docker compose -f $(DC_FILE) exec api /bin/sh

# -------------------------------
# Pre-commit
# -------------------------------
.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files

# -------------------------------
# Versioning
# -------------------------------
.PHONY: version
version:
	@echo $(VERSION)

# -------------------------------
# Dev Bootstrapping
# -------------------------------
.PHONY: dev
dev: install lint test

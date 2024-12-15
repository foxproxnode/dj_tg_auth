# Set the default goal if no targets were specified on the command line
.DEFAULT_GOAL = run
# Makes shell non-interactive and exit on any error
.SHELLFLAGS = -ec

help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

docker-run:
	python manage.py migrate
	python manage.py start_bot &
	gunicorn --workers=2 config.wsgi:application --bind=0.0.0.0:80

migrate:  ## Migrate database to the latest version
	poetry run python3 manage.py migrate

test:  ## Run tests
	poetry run python3 manage.py test

restart: ## Restart project
	docker compose down
	docker compose build
	docker compose up -d
	docker image prune --force

start: ## Start project
	docker compose down
	docker compose build
	docker compose up -d
	docker image prune --force

stop: ## Stop project
	docker compose down

.PHONY: \
  help \
  docker-run \
  migrate \
  test \
  restart \
  start

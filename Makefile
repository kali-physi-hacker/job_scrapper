.PHONY: dev backend frontend worker beat migrate superuser

dev: ## Run both backend and frontend dev servers (requires two shells)
	@echo "Open two terminals: make backend and make frontend"

backend: ## Run Django dev server
	python backend/manage.py runserver

migrate: ## Apply DB migrations
	python backend/manage.py makemigrations && python backend/manage.py migrate

superuser: ## Create Django admin user
	python backend/manage.py createsuperuser

worker: ## Celery worker
	celery -A config.celery_app worker -l info

beat: ## Celery beat scheduler
	celery -A config.celery_app beat -l info


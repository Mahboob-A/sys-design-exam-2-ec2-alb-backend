
#### Docker management commands 
docker-up:
	docker compose -p todo_app_backend -f dev.yml up --build -d --remove-orphans 

docker-down:
	docker compose -p todo_app_backend -f dev.yml down

docker-down-v:
	docker compose -p todo_app_backend -f dev.yml down -v

docker-logs:
	docker compose -p todo_app_backend -f dev.yml logs 

docker-logs-todoapp-api:
	docker compose -p todo_app_backend -f dev.yml logs todoapp-api

docker-restart-todoapp-api:
	docker compose -p todo_app_backend -f dev.yml restart todoapp-api

docker-exec-todoapp-api:
	docker compose -p todo_app_backend -f dev.yml exec todoapp-api /bin/bash 

docker-check-deploy:
	docker compose -p todo_app_backend -f dev.yml run --rm todoapp-api python manage.py check --deploy


# ### Docker Volume and Postgres Database 
docker-exec-postgres: 
	docker compose -p todo_app_backend -f dev.yml exec postgres /bin/bash 

todoapp-database: 
	docker compose -p todo_app_backend -f dev.yml exec postgres psql --username="$(POSTGRES_USER)" --dbname="$(POSTGRES_DB)" 


# ### Services logs commands 
docker-logs-postgres: 
	docker compose -p todo_app_backend -f dev.yml logs postgres


# ### Django Commands
makemigrations: 
	docker compose -p todo_app_backend -f dev.yml run --rm todoapp-api python manage.py makemigrations

migrate: 
	docker compose -p todo_app_backend -f dev.yml run --rm todoapp-api python manage.py migrate

collectstatic: 
	docker compose -p todo_app_backend -f dev.yml run --rm todoapp-api python manage.py collectstatic --no-input --clear 

superuser: 
	docker compose -p todo_app_backend -f dev.yml run --rm todoapp-api python manage.py createsuperuser 

#!/bin/bash 

set -o errexit 
set -o nounset 

python /home/todoapp/app/manage.py makemigrations --no-input 
python /home/todoapp/app/manage.py migrate --no-input 
python /home/todoapp/app/manage.py collectstatic --no-input  

# PORT: 8000. 
exec /usr/local/bin/gunicorn Docker_Todo_App.wsgi:application --bind 0.0.0.0:8000 --chdir=/home/todoapp/app

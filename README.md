# pugorugh_api
This app helps potential pet owners find the dog of their dreams!


#Installation:

git clone <project>

1. Docker:
a) docker build .
b) docker-compose build
c) docker-compose up
d) to access postgresql database:  docker-compose exec db psql --username=postgres --dbname=postgres

2. Virtualenv
a) python3 -m venv env
b) source ./env/bin/activate
c) pip install --upgrade pip && pip install -r requirements.txt
d) python manage.py migrate
e) python pugorugh/scripts/data_import.py #load sample data
f) python manage.py runserver 0.0.0.0:8000

#                              Dogs Catalog | Python, Django, Django REST framework, React

## Description

This app helps potential pet owners find the dog of their dreams!
You can find project guidelines in project_tasks.md . 
Registered users can set thier dog requirements like gender, age, size, fur and breed

## Technologies and Packages Used in App

* Django
* Postgres and SqLite
* [Django REST framework](https://www.django-rest-framework.org/)
* React

## How to use:

git clone <project>

1. Docker:
* docker-compose up
* to access postgresql database:  docker-compose exec db psql --username=postgres --dbname=postgres

2. Virtualenv:
* python3 -m venv env
* source ./env/bin/activate
* pip install --upgrade pip && pip install -r requirements.txt
* python manage.py migrate
* python pugorugh/scripts/data_import.py (load sample data)
* python manage.py runserver 0.0.0.0:8000

3. Testing:
* coverage run manage.py test pugorugh.tests
* coverage report
* using travis-ci.org for autotesting when code added to github

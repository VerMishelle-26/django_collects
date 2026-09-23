# Collects API

REST API для групповых денежных сборов на Django REST Framework.

## Стек
- Python 3.14, Django 6.1
- Django REST Framework, drf-spectacular (Swagger)
- PostgreSQL / SQLite
- Celery + Redis
- Docker + docker-compose

## Запуск локально
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py mock_data --users 50 --collects 200 --payments 1000
python manage.py runserver
release: python3 manage.py migrate
worker : celery -A ama worker -l info
web: gunicorn ama.wsgi
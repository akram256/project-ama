release: python3 manage.py migrate
worker:celery -A ama worker -l --loglevel=info
web: gunicorn ama.wsgi
web: gunicorn tb.wsgi --log-file -
worker: celery -A tb worker -l info
beat: celery -A tb beat -l info
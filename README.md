# tb

To start Celery:

Three shells needed:

1. celery -A tb worker -l info (in ptf2 virtualserver and tb directory)
    a. OR $ celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler 
2. rabbitmq-server (starts server at local host)
3. Normal virtual server start-up
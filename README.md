# tb

To start Celery:

FOUR shells needed:

1. celery -A tb worker -l info (in ptf2 virtualserver and tb directory)
2. celery -A tb beat -l info
  a. (OR if using databse scheduler): $ celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler 
3. /usr/local/sbin/rabbitmq-server (starts server at local host)
4. Normal virtual server start-up.

Note:
1. RabbitMQ must be installed using Brew ('brew install rabbitmq')


DigitalOcean Deployment:
1. Go ahead and deploy from here to Git Origin (github.com i.e. not Heroku)
2. Once completed deploy, :$ ssh root@192.81.213.31
3. Switch to user stephen :$ su - stephen
4. Now see stephen@itb:~/ 
5. Activate Virutalenv :$ source itbenv/bin/activate
6. Now see (itbenv) stephen@itb:$ 
7. Run following now:
     a. :$ git pull origin master
     b. :$ python manage.py collectstatic
     c. :$ python manage.py migrate
     d. :$ sudo supervisorctl restart tb
8. Should now have the new files in the system.
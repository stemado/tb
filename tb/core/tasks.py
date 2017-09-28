import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from tb.medications.models import MedicationTime
from celery import shared_task
import datetime

#CREATES RANDOM USER ACCOUNTS
#NEED TO PUT THIS IN TO A MODEL FORM
@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)

@shared_task
def task_test():
	print('This celery task is running!')

# CREATES RANDOM MEDICATION TIMES (TESTING PURPOSES)
# @shared_task
# def create_random_user_accounts(total):
#     for i in range(total):
#     	MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeGivenNote='RabbitMQ Test', timeCreated=datetime.datetime.now(), timeMedication_id=1)
#     return '{} random medications created with success!'.format(total)
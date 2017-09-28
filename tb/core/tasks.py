import string

from tb.medications.models import Medication, MedicationTime, MedicationCompletion
from datetime import datetime, timedelta, time
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

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

#TEST PERIODIC CHECK BY CELERY
@periodic_task(run_every=(crontab(minute='*/1')), name="task_test", ignore_result=True)

def task_test():
	print('This celery task is running!')
	logger.info('This is from the logger - the celery task is runnin!')

# CHECK FOR MISSED MEDICATIONS THAT WERE NOT DELIVERED THAT DAY
# PURPOSE: Prevents a medication from being missed, records that it was missed that day
# TODO: UPDATE DATE TO today = date - timedelta(days=1) This allows us to check yesterday's records
# (CONTINUED) AT 12:01 AT AND SEE IF ANY WERE MISSED
# NOTE: WILL NEED TO REVIST THIS ONCE WE DETERMINE HOW TO HANDLE MEDICATIONS DUE AT 24:00 AND < OR > 1 HOUR TO DELIVER
@periodic_task(run_every=(crontab(minute=0, hour=1)), name="check_missed_medications", ignore_result=True)
def check_missed_medications():

	date = datetime.now().date()
	yesterday = date - timedelta(days=1)

	for e in MedicationTime.objects.filter(timeDue=None):
		for f in e.completion.filter(completionMedication=e.id):
			if e.completion.filter(completionDate=yesterday):
				logger.info('check_missed_medications - PASS')
			else:
				MedicationCompletion.objects.create(completionMissed='True', completionMedication=e, completionRx=e.timeMedication, completionDue=e.timeDue, completionDate=yesterday, completionNote='ERROR: MEDICATION WAS NOT DELIVERED')
				logger.info('check_missed_medications - OBJECT CREATED')


#Checks if record is overdue by comparing completionTime of record with completionDue
#Updates completionMissed to True (if true)
@periodic_task(run_every=(crontab()), name="check_record_overdue", ignore_result=True)
def check_record_overdue():
	now = datetime.now()
	yesterday = now - timedelta(days=1)
	MedicationCompletion.objects.filter(completionTime__gt=F('completionDue')).update(completionMissed='True')

#Resets the medication status delivery to False at 12:00:01 AM
#So filters work correctly for new day
@periodic_task(run_every=(crontab(minute=1, hour=0)), name="reset_medication_delivery", ignore_result=True)
def reset_medication_delivery():
	MedicationTime.objects.update(timeGivenStatus='False', is_notified=False)




# CREATES RANDOM MEDICATION TIMES (TESTING PURPOSES)
# @shared_task
# def create_random_user_accounts(total):
#     for i in range(total):
#     	MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeGivenNote='RabbitMQ Test', timeCreated=datetime.datetime.now(), timeMedication_id=1)
#     return '{} random medications created with success!'.format(total)
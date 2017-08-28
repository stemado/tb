from datetime import timedelta
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# import sendgrid
# import os
# from sendgrid.helpers.mail import *
from django.core.mail import send_mail
from django.contrib.auth.models import User
from careplus.medications.models import Medication, MedicationCompletion, MedicationTime
from careplus.residents.models import Resident
from careplus.medications.tasks import send_test_email



#This reads when the MedicationComplation form is saved. 
#When saved, signal is sent and updates the medicationStatus to True. 
#Meaning this medication has had action taken on it.
@receiver(post_save, sender=MedicationCompletion)
def check_medication_status(sender, instance, created, **kwargs):

	if created:
		a = instance.completionMedication_id
		b = MedicationTime.objects.get(id=a)
		c = b.timeGivenStatus = 'True'
		b.save()


#Update the completiontime object with the parent timeDue for reporting
#purposes.
@receiver(post_save, sender=MedicationCompletion)
def f(sender, instance, created, **kwargs):

		a = instance.completionMedication_id
		b = MedicationTime.objects.filter(id=a).values_list('timeDue', flat=True)
		MedicationCompletion.objects.filter(id=instance.id).update(completionDue=b[0])



#Subtracts medication count each time medication given. Once medication reaches >= 5, then medication signal is fired off with email to pharmacy requesting refill for 
#patien't medication (tihs will be updated for users to choose how many days until the notificatino is sent (5 by default at ths time.)
@receiver(post_save, sender=MedicationCompletion)	
def update_medication_count(sender, instance, created, **kwargs):	

	if created:
		a = instance.completionMedication_id
		b = MedicationTime.objects.filter(id=a).values('timeMedication_id')
		if instance.completionStatus == True:
			Medication.objects.filter(id=b).update(medicationQuantity=F('medicationQuantity') -1)

#This code cheks the recent creation of the medication and if any of the medicationTimeSchedule 1-6 are not null,then take the value in there and create a new medicationTime
#The medicationTime was the easiest way to split the medication in to bite sized chunks of pills to make the MAR work as needed. Note, at the very end, you will see 
#medicationDistribution = '0', this means the medication is a PRN and only one needs to be created and timeDue is None since it is PRN and must always be present.

@receiver(post_save, sender=Medication, dispatch_uid='medication_time_add')
def create_medication_time(sender, instance, created, **kwargs):

	if created:
		time = timezone.now()
		a = instance.id
		b = instance.medicationTimeSchedule
		c = instance.medicationTimeSchedule2
		d = instance.medicationTimeSchedule3
		e = instance.medicationTimeSchedule4
		f = instance.medicationTimeSchedule5
		g = instance.medicationTimeSchedule6
		if instance.medicationTimeSchedule != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule2 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=c, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule3 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=d, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule4 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=e, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule5 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=f, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule6 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=g, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationFrequency == '0':
			MedicationTime.objects.create(timeStatus=None, timePRN=True, timeGivenStatus=None, timeCreated=time, timeDue=None, timeMedication_id=a, timeGivenNote='Auto Generated - PRN')


#This line of code was fun. In order for the MAR form to fill out correctly, I had to have fillers for the dates existed
#before the medication was started. Example (without this code) if the medication start date waas 7/15/2017, then when the MAR form goes through its loops,
#the first record would be placed under the 1st of the month. This is incorrect since the medication should start on the 15th of the month. 
#to solve this, I created this signal which is fired whenever a new medicationTime is created.
#It (1) gets the startDate of the medication from the medicationTime (2) strips the day from it (3) converts it to an integer (4) checks if the integer (days)
#is greater than 1 (i.e. the first of the month) (5) if it is, then create c - 1 many records to fill the void.
#This allows for the loop to fill in the correct dates with the correct dates in the MAR. Problem solved
#Note, I will probably look back on this in a few months or weeks and think this was a completely stupid way to do this, but it solves my problem at this point.
#One issue, that Celery may be able to solve, is the Model.objects.latest(). This works great if there isonly one person entering medication, but what
#happens if two pepole simultaneously enter different medications? Is it possible person a will get person b's latest medication from the DB (note, the latest is to retrieve
#the most recently created medication. Since the medication kicks off the medicationTime creation signal, and the creation of the medicationTime kicks off this signal,
#then there is a possibility - it seems - that you could have incorrect medication returned. This, again, is only an issue if there is more than one. For 
#carePlus home care plus facilities, it shouldn't be given small size of employee base. If we scale this, though, this code will need to be looked further in to.

@receiver(post_save, sender=MedicationTime)
def create_medication_time_fill(sender, instance, created,  **kwargs):

	if created:
		med = Medication.objects.latest('medicationStartDate')
		a = med.medicationStartDate
		b = a.strftime('%d')
		c = int(b)
		time = timezone.now()
		d = instance.id
		if c > 1:
			while (c > 1):
				c = c - 1
				aa = a - timedelta(days=c)
				print("THIS IS FROM SIGNAL" + str(aa))
				fillRxTime = MedicationCompletion(completionStatus=None, completionDate=aa, completionDue=instance.timeDue, completionNote='SYSTEM RX PLACEHOLDER FILL', completionRx_id=med.id, completionMedication_id=instance.id)
				fillRxTime.save()

##########################################
###########Sendgrid Email Signals#########
##########################################

#Request Refill Signal - Needs some tweaking. 
@receiver(post_save, sender=MedicationCompletion, dispatch_uid='medication_refill')
def request_medication_refill(sender, instance, created, **kwargs):

	med = Medication.objects.get(id=instance.completionRx_id)
	count = med.medicationQuantity
	print(count)
	if created:
		if count == 5:
			email = 'stemado@outlook.com'
			subject = 'Rx Refill Request: ' + str(med.medicationResident)
			content = "Resident: " + str(med.medicationResident) + "needs Medication " + str(med.medicationName) + " refilled. Remaining Pill Count: " + str(med.medicationQuantity)
			send_mail(
				subject, 
				content, 
				'no-reply@careplus.com', 
				[email], 
				fail_silently=False
				)
			print('EMAIL SENT!')
		if count == 1:
			email = 'stemado@outlook.com'
			subject = 'URGENT: Rx Refill Request: ' + str(med.medicationResident)
			content = "Resident: " + str(med.medicationResident) + "needs Medication " + str(med.medicationName) + " refilled. Remaining Pill Count: " + str(med.medicationQuantity)
			send_mail(
				subject, 
				content, 
				'no-reply@careplus.com', 
				[email], 
				fail_silently=False
				)
			print('URGENT EMAIL SENT!')
		else:
			print('It didn not send, home skillet.')

# @receiver(post_save, sender=Medication)
# def new_test_email(sender, instance, created, **kwargs):

# 	if created:
# 		send_test_email.delay(each)
# 		print('Celery email is delayed...now what?')

# 	else:
# 		print('Well, this did not work. Try again tomorrow')


#################################################
############## TWILIO SIGNALS ###################
#################################################



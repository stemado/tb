from django.core.management.base import BaseCommand, CommandError
from tb.medications.models import Medication, MedicationTime, MedicationCompletion
from datetime import datetime, timedelta, time

class Command(BaseCommand):
	help = 'Check that a medicationcompletion record exists for current day. If not, create one.'

	def handle(self, *args, **options):

		today = datetime.now().date()
		# # time = MedicationTime.objects.all().count()
		# time = MedicationTime.objects.filter(completionDue=)
		# record = MedicationCompletion.objects.filter(completionDue=now).count()
		# exist = MedicationTime.completion.exists()

		for e in MedicationTime.objects.all():
			print (e.timeMedication)
			for f in e.completion.filter(completionDue=today):
				if f.medicationCompletion = e.id
				print ('PASS')

		# MedicationCompletion.objects.create(completionMissed='True', completionMedication=e.id, completionRx=e.timeMedication, completionNote='ERROR: MEDICATION WAS NOT DELIVERED')




			

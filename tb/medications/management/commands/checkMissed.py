from django.core.management.base import BaseCommand, CommandError
from tb.medications.models import Medication, MedicationTime, MedicationCompletion
from datetime import datetime, timedelta, time

class Command(BaseCommand):
	help = 'Check that a medicationcompletion record exists for current day. If not, create one.'

	def handle(self, *args, **options):

		date = datetime.now().date()
		today = str(date)
		# # time = MedicationTime.objects.all().count()
		# time = MedicationTime.objects.filter(completionDue=)
		# record = MedicationCompletion.objects.filter(completionDue=now).count()
		# exist = MedicationTime.completion.exists()

		for e in MedicationTime.objects.all():
			print(today)
			print(e.timeMedication)
			for f in e.completion.filter(completionMedication=e.id):
				if e.completion.filter(completionDate=today):
					print('PASS')
				else:
					MedicationCompletion.objects.create(completionMissed='True', completionMedication=e, completionRx=e.timeMedication, completionDue=e.timeDue, completionNote='ERROR: MEDICATION WAS NOT DELIVERED')
					print('OBJECT CREATED')




			# for f in e.completion.filter(completionMedication=e.id):
			# 	if f.completionMedication_id == e.id:
			# 		print('PASS')
			# 	else:
			# 		MedicationCompletion.objects.create(completionMissed='True', completionMedication=e.id, completionRx=e.timeMedication_id, completionDue=e.timeDue, completionNote='ERROR: MEDICATION WAS NOT DELIVERED')
			# 		print('OBJECT CREATED')



			# for f in e.completion.filter(completionDate=today):
			# 	if f.completionMedication_id == e.id:
			# 		print('PASS')
			# 	else:
			# 		MedicationCompletion.objects.create(completionMissed='True', completionMedication=e.id, completionRx=e.timeMedication_id, completionDue=e.timeDue, completionNote='ERROR: MEDICATION WAS NOT DELIVERED')
			# 		print('OBJECT CREATED')



			

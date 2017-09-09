from django.core.management.base import BaseCommand, CommandError
from tb.medications.models import Medication, MedicationTime
from datetime import datetime
from datetime import timedelta

class Command(BaseCommand):
	help = 'Resets the medication status delivery to False at 12:00:01 AM'

	def handle(self, *args, **options):

		now = datetime.now()
		medication = MedicationCompletion.objects.filter(completionDate=now)
		if medication == Null:
			MedicationTime.objects.filter(completion='False', timeDue__lte=hourAfter).update(completionMissed='True')
from django.core.management.base import BaseCommand, CommandError
from tb.medications.models import Medication, MedicationTime, MedicationCompletion
from datetime import datetime
from datetime import timedelta
from django.db.models import signals, Count, Q, F


class Command(BaseCommand):
	help = 'Resets the medication status delivery to False at 12:00:01 AM'

	def handle(self, *args, **options):

		now = datetime.now()
		yesterday = now - timedelta(days=1)
		MedicationCompletion.objects.filter(completionTime__gt=F('completionDue')).update(completionMissed='True')
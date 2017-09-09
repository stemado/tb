from django.core.management.base import BaseCommand, CommandError
from tb.medications.models import Medication, MedicationTime
from datetime import datetime

class Command(BaseCommand):
	help = 'Resets the medication status delivery to False at 12:00:01 AM'

	def handle(self, *args, **options):

		MedicationTime.objects.update(timeGivenStatus='False')
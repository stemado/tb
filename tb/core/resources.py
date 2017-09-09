from import_export import resources
from tb.medications.models import Medication
from django.contrib.auth.models import User

class MedicationResource(resources.ModelResource):
	class Meta:
		model = Medication

class PatientResource(resources.ModelResource):
	class Meta:
		model = User
from django.contrib.auth.models import User
import django_filters
from tb.medications.models import Medication

class MedicationFilter(django_filters.FilterSet):
    class Meta:
        model = Medication
        fields = {
            'medicationName': ['contains'],
            'medicationStartDate': ['exact'],
            'medicationQuantity': ['exact'],
            'patient': ['contains'], 
 
        	}
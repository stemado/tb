from django.contrib.auth.models import User
from rest_framework import serializers
from tb.medications.models import Medication

class MedicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email')
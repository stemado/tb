from django.contrib.auth.models import User
from rest_framework import serializers
from tb.medications.models import Medication


## Medication Model Serializer ##
## Determines what the fields will display 
## from the Medication model when the url is called
class MedicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Medication
		fields = (
			'id', 
			'user', 
			'medicationName', 
			'medicationQuantity', 
			'medicationFrequency', 
			'medicationTimeSchedule', 
			'medicationTimeSchedule2', 
			'medicationTimeSchedule3', 
			'medicationTimeSchedule4', 
			'medicationTimeSchedule5'
			)

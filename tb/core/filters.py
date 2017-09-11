from django.contrib.auth.models import User
import django_filters

class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'first_name': ['contains'], 
        	'last_name': ['contains'],
        	'email': ['contains'], 
        	}
from django.contrib.auth.models import User
import django_filters
from tb.authentication.models import Profile

class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = {
            'id': ['contains'], 
        	'user': ['exact'], 
        	}
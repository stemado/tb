
from django import forms

from careplus.residents.models import Resident, EmergencyContact
from django.utils.translation import ugettext_lazy as _


class ResidentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResidentForm, self).__init__(*args, **kwargs)
        self.fields['residentFirstName'].required = True
        self.fields['residentLastName'].required = True
        self.fields['residentProfile'].required = False
        self.fields['residentSSN'].required = True
        self.fields['residentDOB'].required = True
        self.fields['residentPrimaryPhysician'].required = True
        self.fields['location'].required = True
        self.fields['medicareNumber'].required = True
        self.fields['dnr_status'].required = True
        self.fields['residentStatus'].required = True
    

    class Meta:
        model = Resident
        fields = ['residentFirstName', 'residentLastName', 'residentProfile', 'residentSSN', 'residentDOB', 'residentPrimaryPhysician', 'location', 'medicareNumber', 'dnr_status', 'residentStatus']


class EmergencyContactForm(forms.ModelForm):
    emergencyContactFirstName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    emergencyContactLastName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    emergencyContactRelationship = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=9)
    emergencyContactPhoneNumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=10)
    resident = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    

    class Meta:
        model = EmergencyContact
        fields = ['emergencyContactFirstName', 'emergencyContactLastName', 'emergencyContactRelationship', 'emergencyContactPhoneNumber', 'resident']


from django import forms
from django.utils.translation import gettext_lazy as _
from tb.medications.models import Medication, MedicationCompletion, MedicationTime
from extra_views import InlineFormSet
from django.forms import ModelForm
from datetime import datetime
from django.contrib.auth.models import User


class MedicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicationForm, self).__init__(*args, **kwargs)
        self.fields['medicationName'].required = True
        self.fields['medicationDosage'].required = True
        self.fields['medicationFrequency'].required = True
        self.fields['medicationStartDate'].required = True
        self.fields['medicationDosage'].required = True
        self.fields['medicationQuantity'].required = True
        self.fields['medicationType'].required = True
        self.fields['medicationDiscontinuedStatus'].required = True
        self.fields['patient'].required = False
        self.fields['user'].required = True

    patient = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control patient'}),
        max_length=30,
        required=False)

    user = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control resident'}),
        max_length=30,
        required=False)

    class Meta:
        model = Medication
        fields = ['medicationName', 'medicationDosage', 'medicationFrequency', 'medicationStartDate',  'medicationTimeSchedule', 'medicationTimeSchedule2', 'medicationTimeSchedule3', 'medicationTimeSchedule4', 'medicationTimeSchedule5', 'medicationTimeSchedule6',  'medicationQuantity', 'medicationType', 'medicationDiscontinuedStatus', 'medicationComment', 'patient', 'user']


# class StatusForm(forms.ModelForm):

#     class Meta:
#         model = MedicationCompletion
#         fields = ['completionStatus', 'completionStatus2', 'completionNote', 'completionMedication']

class StatusForm(forms.ModelForm):


    class Meta:
        model = MedicationCompletion
        fields = ['completionStatus', 'completionRx', 'completionNote', 'completionMedication', 'completionDate']

class MedicationStatusForm(forms.ModelForm):

    medicationName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)

    medicationComment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=500)



class StatusFormSet(InlineFormSet):
    model = MedicationCompletion
    max_num = 1

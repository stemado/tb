
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
        self.fields['patient'].widget.attrs['disabled'] = True
        self.fields['user'].widget.attrs['disabled'] = False

#Have to figure out how to pass the user field as an instance. 
#It wont' let me with custom field. Have to remove formatting so it uses default.
    # medicationTimeSchedule = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control medicationTime'}),
    #     max_length=30,
    #     required=False)

    # medicationTimeSchedule2 = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control medicationTime'}),
    #     max_length=30,
    #     required=False)
    medicationStartDate = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}))

    class Meta:
        model = Medication
        fields = ['medicationName', 'medicationDosage', 'medicationFrequency', 'medicationStartDate',  'medicationTimeSchedule', 'medicationTimeSchedule2', 'medicationTimeSchedule3', 'medicationTimeSchedule4', 'medicationTimeSchedule5', 'medicationTimeSchedule6',  'medicationQuantity', 'medicationType', 'medicationDiscontinuedStatus', 'medicationComment', 'patient', 'user']


# class StatusForm(forms.ModelForm):

#     class Meta:
#         model = MedicationCompletion
#         fields = ['completionStatus', 'completionStatus2', 'completionNote', 'completionMedication']

class StatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['completionRx'].is_hidden = True
        self.fields['completionMedication'].is_hidden = True
        self.fields['completionDue'].is_hidden = True


# Note: completionRx and completionMedication are not customized like the below because
# they require objects. If you add them to the below, then you will get an error of
# completionMedication/completionRx needs to be instance of MedicationTime/Medication
# since they are hidden fields anyway, there is no need to clean them up
# aesthetically.
    completionNote = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False,
        label="Note:")
    completionDate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=50,
        required=False)
    completionDue = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        required=False)


    class Meta:
        model = MedicationCompletion
        fields = ['completionStatus', 'completionRx', 'completionNote', 'completionMedication', 'completionDate', 'completionDue']

class EditStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditStatusForm, self).__init__(*args, **kwargs)
        self.fields['completionRx'].is_hidden = True
        self.fields['completionMedication'].is_hidden = True
        self.fields['completionDue'].is_hidden = True
        self.fields['completionDate'].is_hidden = False
        self.fields['completionMissed'].widget.attrs['disabled'] = True


# Note: completionRx and completionMedication are not customized like the below because
# they require objects. If you add them to the below, then you will get an error of
# completionMedication/completionRx needs to be instance of MedicationTime/Medication
# since they are hidden fields anyway, there is no need to clean them up
# aesthetically.
    completionNote = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=True,
        label="Edit Note:")

    completionMissed = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=9,
        required=False)

    completionDate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control user-type'}),
        max_length=50,
        required=False)


    class Meta:
        model = MedicationCompletion
        fields = ['completionStatus', 'completionRx', 'completionNote', 'completionMedication', 'completionDate', 'completionDue']

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

from __future__ import unicode_literals
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView
from django.template.defaultfilters import slugify
import bleach
from tb.activities.models import Activity
from django_filters import ModelMultipleChoiceFilter
from django_filters import rest_framework as filters
from django.utils import timezone
from django.db.models import signals, Count, Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import signals
from itertools import chain
from operator import attrgetter
from django.core.mail import send_mail
import django_tables2 as tables

class MedicationQuerySet(models.QuerySet):

    def medicationDeliveryTime(self):

        now = datetime.now()
        hourBefore = now - timedelta(hours=1)
        hourAfter = now + timedelta(hours=1)
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)


        return self.filter(medicationTimeSchedule__range=(hourBefore, hourAfter))

    def medicationDeliveryTime(self):

        now = datetime.now()
        hourBefore = now - timedelta(hours=1)
        hourAfter = now + timedelta(hours=1)

        return self.filter(medicationTimeSchedule__range=(hourBefore, hourAfter))

    def medicationDeliveryStatus(self):
        return self.filter(medicationStatus='False')

    def medicationDeliveryOverdue(self):

        now = datetime.now()
        hourAfter = now - timedelta(hours=1, minutes=1)
        currentDay = now - timedelta()

        return self.filter(medicationTimeSchedule__lte=(hourAfter))

    def medicationDeliveryOverdue2(self):

        now = datetime.now()
        hourAfter = now - timedelta(hours=1, minutes=1)
        currentDay = now - timedelta()

        return self.filter(medicationTimeSchedule2__lte=(hourAfter))

class MedicationManager(models.Manager):
    def get_queryset(self):
        return MedicationQuerySet(self.model, using=self._db)

    def medicationDeliveryTime(self):
        return self.get_queryset().medicationDeliveryTime()

    def medicationDeliveryStatus(self):
        return self.get_queryset().medicationDeliveryStatus()

    def medicationDeliveryOverdue(self):
        return self.get_queryset().medicationDeliveryOverdue()

    def medicationDeliveryOverdue2(self):
        return self.get_queryset().medicationDeliveryOverdue2()

    def medicationReset(self):
        return self.get_queryset().medicationReset()



@python_2_unicode_compatible
class Medication(models.Model):

    MISSED_CHOICES = (('False', 'False'), ('True', 'True'))
    DISCONTINUED_CHOICES = (('Active', 'Active'), ('Discontinued', 'Discontinued'))
    DISTRUBUTION_CHOICES = (('0', 'PRN - As Needed'), ('1', 'QD - 1 Times A Day'), ('2', 'BID - 2 Times A Day'), ('3', 'TID - 3 Timse A Day'), ('4', 'QID - 4 times a day'), ('5', 'SID - 5 times a day'), ('6', '6 times a day'))

    medicationName = models.CharField(verbose_name="Medication Name", default="Medication", max_length=50, null=True, blank=True)
    medicationSlug = models.SlugField(verbose_name="Slug", max_length=255, null=True, blank=True)
    medicationDosage = models.CharField(verbose_name="Dosage", default="e.g. 120 mg", max_length=50, null=True, blank=True)
    medicationFrequency = models.CharField(verbose_name="Frequency", choices=DISTRUBUTION_CHOICES, max_length=50, null=True, blank=True)
    medicationQuantity = models.IntegerField(verbose_name="Quantity", default="30", null=True, blank=True)
    medicationType = models.CharField(verbose_name="Drug Type", default="Need Options", max_length=20, null=True, blank=True)
    medicationComment = models.CharField(verbose_name="Physician Orders", max_length=500, null=True, blank=True)
    medicationStartDate = models.DateField(verbose_name="Medication Start Date", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule = models.TimeField(verbose_name="Time 1",  blank=True, null=True)
    medicationTimeSchedule2 = models.TimeField(verbose_name="Time 2", blank=True, null=True)
    medicationTimeSchedule3 = models.TimeField(verbose_name="Time 3", blank=True, null=True)
    medicationTimeSchedule4 = models.TimeField(verbose_name="Time 4", blank=True, null=True)
    medicationTimeSchedule5 = models.TimeField(verbose_name="Time 5", blank=True, null=True)
    medicationTimeSchedule6 = models.TimeField(verbose_name="Time 6", blank=True, null=True)
    medicationDiscontinuedStatus = models.CharField(verbose_name="DC Status", choices=DISCONTINUED_CHOICES, max_length=15, default='Active', blank=True, null=True)
    medicationDateTimeAdded = models.DateTimeField(auto_now_add=True)
    medicationMissed = models.CharField(verbose_name="Medication Missed", choices=MISSED_CHOICES, max_length=12, default='False', blank=True, null=True)
    medicationRecordReset = models.DateTimeField(default=datetime.now, blank=True, null=True)
    user = models.ForeignKey(User)
    patient = models.CharField(verbose_name="Patient", max_length=50, blank=True, null=True)

    
    objects = MedicationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Medication")
        verbose_name_plural = _("Medications")
        ordering = ('-medicationName',)


  
    def __str__(self):
        return (self.medicationName)

    # def completion_medication_set():
    #     a = Medication.objects.filter(medicationResident=1)
    #     b = a.medicationtime_set.all()
    #     medication = b.completion.all()
    #     return medication

    def get_all_medications():
        medications = MedicationTime.objects.all().order_by('medication_id')
        return medications

    def get_medications():
        medications = Medication.objects.filter(medicationDiscontinuedStatus='Active')
        return medications


    ##Chain Query Examples##
    # def get_overdue_medications():
    #     now = datetime.now()
    #     hourAfter = now - timedelta(hours=1, minutes=1)
    #     a = TimeMedicationOne.objects.filter(timeStatus2='False', timeTime__lte=hourAfter)
    #     b = TimeMedicationTwo.objects.filter(timeStatus2='False', timeTime__lte=hourAfter)
    #     medication = list(chain(a,b))
    #     return medication




 
    def get_medication(self):
        return Medication.objects.filter(medication=self)



@python_2_unicode_compatible
class MedicationTable(tables.Table):
    class Meta:
        model = Medication

@python_2_unicode_compatible
class MedicationTime(models.Model):

    BOOL_CHOICES = ((True, 'Accepted'), (False, 'Refused'))
    MISSED_CHOICES = (('False', 'False'), ('True', 'True'))
    STATUS_CHOICES = (('Null', 'Null'), ('False', 'False'), ('True', 'True'))

    timeDue = models.TimeField(verbose_name="Time Due", null=True, blank=True)
    timeDelivered = models.TimeField(verbose_name="Time Delivered", null=True, blank=True)
    timeStatus = models.NullBooleanField(verbose_name="Medication", choices=BOOL_CHOICES, default=None, null=True, blank=True)
    timeGivenStatus = models.CharField(verbose_name="Given", choices=STATUS_CHOICES, default=None,max_length=12, null=True, blank=True)
    timeGivenDate = models.DateTimeField(verbose_name="Date Added", auto_now_add=True)
    timeGivenNote = models.CharField(verbose_name="Notes", max_length=500, null=True, blank=True)
    timePRN = models.NullBooleanField(verbose_name="PRN?", default=None, null=True, blank=True)
    timeCreated = models.DateTimeField(verbose_name="Created")
    timeMedication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)
 
    def __str__(self):
        return '%s %s' % (self.timeMedication, self.timeDue)

    def get_status(self):
        return MedicationCompletion.objects.filter(completionMedication=self)

    def get_all_times():
        medication = MedicationTime.completion.all()
        return medication

    def get_overdue_medications():
        now = datetime.now()
        nextDay = now + timedelta(days=1)
        hourAfter = now - timedelta(hours=1, minutes=1)
        medication = MedicationTime.objects.filter(timeGivenStatus='False', timeDue__lte=hourAfter)
        return medication

    def get_active_medications():
        now = datetime.now()
        hourBefore = now - timedelta(hours=1)
        hourAfter = now + timedelta(hours=1)
        medication = MedicationTime.objects.filter(timeGivenStatus='False', timeDue__range=(hourBefore, hourAfter))
        return medication

    def get_prn_medications():
        medication = MedicationTime.objects.filter(timePRN=True)
        return medication



@python_2_unicode_compatible
class MedicationCompletion(models.Model):

    BOOL_CHOICES = ((True, 'Accepted'), (False, 'Refused'))
    MISSED_CHOICES = (('False', 'False'), ('True', 'True'))
    STATUS_CHOICES = (('Null', 'Null'), ('False', 'False'), ('True', 'True'))
    TIME_CHOICES = (('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'))

    completionStatus = models.NullBooleanField(verbose_name="Current Status", choices=BOOL_CHOICES, default=None, null=True, blank=True)
    completionStatus2 = models.CharField(verbose_name="Current Status 2", choices=STATUS_CHOICES, default='Null', max_length=12, null=True, blank=True)
    completionMissed = models.CharField(verbose_name="Medicaton Missed", choices=MISSED_CHOICES, default='False', max_length=12, null=True, blank=True)
    completionMissed = models.CharField(verbose_name="Medicaton Missed", choices=MISSED_CHOICES, default='False', max_length=12, null=True, blank=True)
    completionEdited = models.CharField(verbose_name="Medicaton Edited", max_length=50, null=True, blank=True)    
    completionEditedUser = models.CharField(verbose_name="Edited by:", max_length=50, null=True, blank=True)
    completionEditedDate = models.CharField(verbose_name="Date by:", max_length=50, null=True, blank=True)
    completionTime = models.TimeField(verbose_name="Time Given", auto_now_add=True)
    completionDue = models.TimeField(verbose_name="Time Due", null=True, blank=True)
    completionDate = models.DateField(verbose_name="Date Given")
    completionNote = models.CharField(verbose_name="Note", max_length=500, null=True, blank=True)    
    completionMedication = models.ForeignKey(MedicationTime, related_name="completion", on_delete=models.CASCADE)
    completionRx = models.ForeignKey(Medication, related_name="mymedication", on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.completionRx, self.completionMissed)


    def get_monthly_missed():
        today = datetime.now()
        missed = MedicationCompletion.objects.filter(completionDate__contains=today.month, completionMissed=True)
        return missed
    
    def get_monthly_delivered():
        today = datetime.now()
        delivered = MedicationCompletion.objects.filter(completionDate__contains=today.month)
        return delivered

@python_2_unicode_compatible
class MedicationCompletionChangeHistory(models.Model):

    user = models.ForeignKey(User)
    medicationRx = models.ForeignKey(Medication)
    medicationTime = models.ForeignKey(MedicationTime)
    dateEdited = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.medicationRx, self.medicationTime)




class SendSMS(models.Model):
    to_number = models.CharField(max_length=30)
    from_number = models.CharField(max_length=30)
    sms_sid = models.CharField(max_length=34, default="", blank=True)
    account_sid = models.CharField(max_length=34, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="", blank=True)
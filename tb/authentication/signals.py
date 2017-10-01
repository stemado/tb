import os
from datetime import timedelta
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from decouple import Csv, config
from django.core.mail import send_mail
from tb.authentication.models import Profile
from twilio.rest import Client

#Create user patient record when user profile created.
@receiver(post_save, sender=Profile)
def create_patient(sender, instance, created, **kwargs):
	if created:
		user = Profile.objects.get(id=instance.id)
		Patient.objects.create(patient_id=, first_name=instance.first_name, last_name=instance.last_name, email=instance.email, city=instance.city, providence=instance.providence, zipcode=instance.zipcode, address1=instance.address1, address2=instance.address2, phonenumber=instance.phonenumber, mobilenumber=instance.mobilenumber, profile=instance.id)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
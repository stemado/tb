from __future__ import unicode_literals
import hashlib
import os.path
import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from tb.activities.models import Notification

@python_2_unicode_compatible
class Profile(models.Model):

    AUTH_CHOICES = (('0', 'Administrator'), ('1', 'Patient'))

    user = models.OneToOneField(User)
    city = models.CharField(max_length=20, null=True, blank=True)
    providence = models.CharField(max_length=20, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.CharField(max_length=20, null=True, blank=True)
    address2 = models.CharField(max_length=20, null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    mobilenumber = models.CharField(max_length=20, null=True, blank=True, unique=True)
    pharmacy = models.CharField(max_length=20, null=True, blank=True)
    pinnumber = models.CharField(max_length=4, unique=True, null=True)
    emailnotify = models.NullBooleanField(default=True, blank=True)
    smsnotify = models.NullBooleanField(default=True, blank=True)
    user_type = models.CharField(max_length=20, default='Patient', choices=AUTH_CHOICES)


    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username


    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                    )
                return gravatar_url

        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user, to_user=feed.user,
                                        feed=feed).delete()

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)

        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user,
                         to_user=User(id=user), feed=feed).save()

    def notify_favorited(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.FAVORITED,
                         from_user=self.user, to_user=question.user,
                         question=question).save()

    def unotify_favorited(self, question):
        if self.user != question.user:
            Notification.objects.filter(
                notification_type=Notification.FAVORITED,
                from_user=self.user,
                to_user=question.user,
                question=question).delete()

    def notify_answered(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    def notify_accepted(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.ACCEPTED_ANSWER,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

    def unotify_accepted(self, answer):
        if self.user != answer.user:
            Notification.objects.filter(
                notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user,
                to_user=answer.user,
                answer=answer).delete()

    def notify_new_resident(self, new_resident):
        if self.user == answer.user:
            Notification(notification_type=Notification.NEW_RESIDENT,
                         from_user=self.user,
                         to_user=answer.user,
                         new_resident=new_resident).save()

    def unotify_new_resident(self, new_resident):
        if self.user == answer.user:
            Notification.objects.filter(
                notification_type=Notification.NEW_RESIDENT,
                from_user=self.user,
                to_user=answer.user,
                new_resident=new_resident).delete()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)





##Add Signal to Create A New Patient For the Patient Table When New User Created That is Patient
#This will allow me to continue using the Django built in User Authentication system.
#Probably a better way, this will work for now.
@python_2_unicode_compatible
class Patient(models.Model):

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    providence = models.CharField(max_length=20, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.CharField(max_length=20, null=True, blank=True)
    address2 = models.CharField(max_length=20, null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    mobilenumber = models.CharField(max_length=20, null=True, blank=True)
    profile = models.ForeignKey(Profile, null=True)



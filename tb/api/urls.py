from django.conf.urls import include, url

from tb.api import views

urlpatterns = [
    url(r'^Medication/$', views.MedicationList),

]

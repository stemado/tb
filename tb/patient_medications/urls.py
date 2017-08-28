
from django.conf.urls import url

from careplus.residents import views

urlpatterns = [

	url(r'^$', views.residents, name='residents'),
	url(r'^(?P<id>[0-9]+)/$', views.resident, name='resident'),
    url(r'^rx_active/(?P<id>[0-9]+)/$', views.rx_active, name='rx_active'),
    url(r'^rx_overdue/(?P<id>[0-9]+)/$', views.rx_overdue, name='rx_overdue'),
    url(r'^rx_prn/(?P<id>[0-9]+)/$', views.rx_prn, name='rx_prn'),
    url(r'^rx_all/(?P<id>[0-9]+)/$', views.rx_all, name='rx_all'),
    url(r'^list/(?P<id>[0-9]+)/$', views.medicationList, name='medicationList'),
    url(r'^create/$', views.create, name='create'),
    url(r'^check/$', views.check_medications, name='check_medications'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^emergency/$', views.emergencycontact, name='emergencycontact'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.deleteResident, name='delete_resident'),
    

]


from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from importlib import reload

from tb.activities import views as activities_views
from tb.authentication import views as tb_auth_views
from tb.core import views as core_views
from tb.search import views as search_views


urlpatterns = [
	url(r'^$', core_views.home, name='home'),
    # The below will replace the current "home" view with "app"
    # to go to the actual app. Home will go to the marketing page.
    url(r'^app/$', core_views.app, name='app'),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
	url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('tb.api.urls')),
    url(r'^login', auth_views.login, {'template_name': 'core/cover.html'},
        name='login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^signup/$', tb_auth_views.signup, name='signup'),
    url(r'^import/$', core_views.importPatients, name='import'),    
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/edit/$', core_views.edit_profile, name='edit_profile'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
 
    url(r'^settings/create/$', core_views.create_medication, name='create_medication'),
    url(r'^settings/upload_picture/$', core_views.upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^network/$', core_views.network, name='network'),
    url(r'^feeds/', include('tb.feeds.urls')),
    url(r'^medications/', include('tb.medications.urls')),
    url(r'^medications/export', core_views.medicationExport, name='export'),
    url(r'^messages/', include('tb.messenger.urls')),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^notifications/$', activities_views.notifications,
        name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^notifications/check/medications/$', activities_views.check_notifications_medication,
        name='check_notifications_medication'),
	url(r'^search/$', search_views.search, name='search'),
    url(r'^profile/$', core_views.profile, name='profile'),
    url(r'^profile/patient/$', core_views.patients, name='patients'),
    url(r'^profile/patient/(?P<id>[0-9]+)/$', core_views.patient_medication, name='patient_medication'),
    url(r'^dashboard/$', core_views.dashboard, name='dashboard'),
    url(r'^medication/$', core_views.medication, name='medication'),
    url(r'^medication/overdue/(?P<id>[0-9]+)/$', core_views.medication_overdue, name='medication_overdue'),
    url(r'^medication/active/(?P<id>[0-9]+)/$', core_views.medication_active, name='medication_active'),
    # url(r'^clinic/$', core_views.clinicReport, name='clinic'),
    url(r'^clinic/$', core_views.clinicReport, name='clinic'),
    url(r'^registration/$', core_views.registration, name='registration'),
    url(r'^registration_tc/$', core_views.registration_page_2, name='registration_tc'),
    url(r'^registration_pharmacy/$', core_views.registration_page_3, name='registration_pharmacy'),
    url(r'^registration_notification/$', core_views.registration_page_4, name='registration_notification'),
    url(r'^users_list/$', core_views.UsersListView.as_view(), name='users_list'),
    url(r'^generate/$', core_views.GenerateRandomUserView.as_view(), name='generate'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
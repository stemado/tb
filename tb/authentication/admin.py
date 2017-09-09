from tb.authentication.models import Profile
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
	pass

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass


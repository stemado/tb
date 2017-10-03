from tb.feeds.models import Feed
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

@admin.register(Feed)
class FeedAdmin(ImportExportModelAdmin):
    pass
from tb.medications.models import Medication, MedicationTime, MedicationCompletion
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin



@admin.register(Medication)
class MedicationAdmin(ImportExportModelAdmin):
    pass


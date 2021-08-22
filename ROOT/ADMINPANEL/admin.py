from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(models.Department_Information)
@admin.register(models.Declare_Result)
class ViewAdmin(ImportExportModelAdmin):
    exclude = ('id', )

from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(models.UserRegistration)
@admin.register(models.Question)
class ViewAdmin(ImportExportModelAdmin):
    exclude = ('id', )

from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(models.FeedbackForm)
@admin.register(models.QuizData)
@admin.register(models.EnrollemntsForQuiz)
@admin.register(models.AllowedEnrollments)
@admin.register(models.UserRegistration)
@admin.register(models.Question)
class ViewAdmin(ImportExportModelAdmin):
    exclude = ('id', )

from django.db import models
from django_pandas.managers import DataFrameManager
# Create your models here.

class UserRegistration(models.Model):

    FIRST_NAME = models.CharField(max_length=100)
    LAST_NAME = models.CharField(max_length=100)
    ENROLLMENT_NUMBER = models.CharField(max_length=100)
    # EMAIL = models.EmailField(max_length = 254)
    # GENDER = models.CharField(max_length=10)
    # SEMESTER = models.IntegerField()
    # SCHOOL= models.CharField(max_length=100)
    # PROGRAM= models.CharField(max_length=100)
    # CONTACT = models.IntegerField()
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.FIRST_NAME}"

class Question(models.Model):
    SR_NO = models.IntegerField()
    CATEGORY = models.CharField(max_length=50)
    QUESTION = models.CharField(max_length=1000)
    CORRECT = models.CharField(max_length=50, blank=True)
    CHOICE_1 = models.CharField(max_length=50)
    CHOICE_2 = models.CharField(max_length=50)
    CHOICE_3 = models.CharField(max_length=50, blank=True)
    CHOICE_4 = models.CharField(max_length=50, blank=True)
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.CATEGORY}-{self.QUESTION}"

"""STUDENTS ENROLLMENT NUMBERS"""
class AllowedEnrollments(models.Model):

    ENROLLMENT_NUMBER = models.CharField(max_length=100,)
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.ENROLLMENT_NUMBER}"

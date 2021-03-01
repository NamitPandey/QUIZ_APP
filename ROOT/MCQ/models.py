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
        return f"{self.ENROLLMENT_NUMBER}-{self.FIRST_NAME}"

class Question(models.Model):

    QUESTION_ID = models.IntegerField()
    CATEGORY = models.CharField(max_length=50)
    QUESTION = models.CharField(max_length=1000)
    CORRECT = models.CharField(max_length=50)
    CHOICE_1 = models.CharField(max_length=50)
    CHOICE_2 = models.CharField(max_length=50)
    CHOICE_3 = models.CharField(max_length=50, blank=True)
    CHOICE_4 = models.CharField(max_length=50, blank=True)
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.CATEGORY}-{self.QUESTION}"

"""STUDENTS ENROLLMENT NUMBERS"""
class EnrollemntsForQuiz(models.Model):

    ENROLLMENT_NUMBER = models.CharField(max_length=100,)
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.ENROLLMENT_NUMBER}"

"""STUDENTS ENROLLMENT NUMBERS TO BE CHECKED WHILE REGISTERING STUDENTS"""
class AllowedEnrollments(models.Model):

    ENROLLMENT_NUMBER = models.CharField(max_length=100,)
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.ENROLLMENT_NUMBER}"

class QuizData(models.Model):

    QUESTION_ID = models.IntegerField()
    ACTUAL_QUESTION = models.CharField(max_length=1000)
    ENROLLMENT_NUMBER = models.CharField(max_length=100)
    CATEGORY = models.CharField(max_length=50)
    ANSWER = models.EmailField(max_length = 254)
    CORRECT_ANSWER = models.CharField(max_length=50)
    # START_TIME = models.DateTimeField(blank=True)
    # END_TIME = models.DateTimeField(blank=True)
    # SEMESTER = models.IntegerField()
    # SCHOOL= models.CharField(max_length=100)
    # PROGRAM= models.CharField(max_length=100)
    # CONTACT = models.IntegerField()
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.QUESTION_ID}-{self.ACTUAL_QUESTION}"

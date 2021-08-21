from django.db import models
from django_pandas.managers import DataFrameManager
from django.utils import timezone
# Create your models here.

class UserRegistration(models.Model):

    FIRST_NAME = models.CharField(max_length=100)
    LAST_NAME = models.CharField(max_length=100)
    ENROLLMENT_NUMBER = models.CharField(max_length=1000)
    EMAIL = models.EmailField(max_length = 500)
    GENDER = models.CharField(max_length=10)
    SEMESTER = models.IntegerField()
    SCHOOL= models.CharField(max_length=100)
    PROGRAM= models.CharField(max_length=100)
    # CONTACT = models.IntegerField()
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.ENROLLMENT_NUMBER}-{self.FIRST_NAME}"

class Question(models.Model):

    QUESTION_ID = models.IntegerField()
    CATEGORY = models.CharField(max_length=150)
    QUESTION = models.CharField(max_length=50000)
    CORRECT = models.CharField(max_length=50000)
    CHOICE_1 = models.CharField(max_length=50000)
    CHOICE_2 = models.CharField(max_length=50000)
    CHOICE_3 = models.CharField(max_length=50000, blank=True)
    CHOICE_4 = models.CharField(max_length=50000, blank=True)
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.CATEGORY}-{self.QUESTION}"

"""STUDENTS ENROLLMENT NUMBERS"""
class EnrollemntsForQuiz(models.Model):

    ENROLLMENT_NUMBER = models.CharField(max_length=1000,)
    START_TIME = models.DateTimeField(default=timezone.now())
    END_TIME = models.DateTimeField(default=timezone.now())
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
    ACTUAL_QUESTION = models.CharField(max_length=50000)
    ENROLLMENT_NUMBER = models.CharField(max_length=1000)
    CATEGORY = models.CharField(max_length=150)
    ANSWER = models.CharField(max_length = 50000)
    SCHOOL= models.CharField(max_length=100)
    PROGRAM= models.CharField(max_length=100)
    CORRECT_ANSWER = models.CharField(max_length=50000)
    START_TIME = models.DateTimeField(auto_now=True)
    END_TIME = models.DateTimeField(auto_now_add=True)
    GENDER = models.CharField(max_length=10)
    SEMESTER = models.IntegerField()
    SCHOOL= models.CharField(max_length=100)
    PROGRAM= models.CharField(max_length=100)
    # CONTACT = models.IntegerField()
    objects = DataFrameManager()

    def __str__(self):
        return f"{self.QUESTION_ID}-{self.CATEGORY}-{self.ACTUAL_QUESTION}"

# class FeedBack_Q3(models.Model):
#
#     CHOICES = (
#         ('I was really surprised to see the questions which I wasn’t aware of','I was really surprised to see the questions which I wasn’t aware of'),
#         ('I feel I need to read a lot on General Knowledge', 'I feel I need to read a lot on General Knowledge'),
#         ('I feel this type of test would help me in my future knowledge bank', 'I feel this type of test would help me in my future knowledge bank'),
#         ('I would like to take such task in future', 'I would like to take such task in future')
#     )
#
#     QSTN_THREE_CHOICES = models.CharField(max_length=500,choices=CHOICES, unique=True)
#
#     def __str__(self):
#         return f"{self.QSTN_THREE_CHOICES}"

class FeedbackForm(models.Model):

    QSTN_ONE = models.CharField(max_length=200)
    QSTN_ONE_ANSWR = models.CharField(max_length=50)
    QSTN_TWO = models.CharField(max_length=200)
    QSTN_TWO_ANSWR = models.CharField(max_length=50)
    QSTN_THREE = models.CharField(max_length=200)
    QSTN_THREE_ANSWR_CHOICE_1 = models.CharField(max_length=850)
    QSTN_THREE_ANSWR_CHOICE_2 = models.CharField(max_length=850, blank=True)
    QSTN_THREE_ANSWR_CHOICE_3 = models.CharField(max_length=850, blank=True)
    QSTN_THREE_ANSWR_CHOICE_4 = models.CharField(max_length=850, blank=True)
    COMMENTS = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return f"{self.QSTN_ONE}-{self.QSTN_TWO}-{self.QSTN_THREE}"

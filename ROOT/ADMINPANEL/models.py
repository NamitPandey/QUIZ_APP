from django.db import models
from django_pandas.managers import DataFrameManager

# Create your models here.
class Declare_Result(models.Model):

    RESULT_STATUS = models.IntegerField(default=0)

    objects = DataFrameManager()

    def __str__(self):

        if self.RESULT_STATUS == 0:

            return f"{self.id}.Result is Not Declared"

        else:
            return f"{self.id}.Result Declared"


class Department_Information(models.Model):

    NAME = models.CharField(max_length=254, blank=False)
    SCHOOL_NAME = models.CharField(max_length=254, blank=False)
    PROGRAM_NAME = models.CharField(max_length=254, blank=False)
    EMAIL_ID = models.EmailField(max_length=254, blank=False)

    def __str__(self):

        return f"{self.NAME}, {self.SCHOOL_NAME}, {self.PROGRAM_NAME}"

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

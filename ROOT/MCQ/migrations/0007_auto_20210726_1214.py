# Generated by Django 3.2.5 on 2021-07-26 12:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCQ', '0006_auto_20210724_2340'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Declare_Result',
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='END_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 12, 14, 5, 454998)),
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='START_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 12, 14, 5, 454945)),
        ),
    ]
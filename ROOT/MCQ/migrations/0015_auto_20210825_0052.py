# Generated by Django 3.2.5 on 2021-08-25 00:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCQ', '0014_auto_20210823_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='END_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 25, 0, 52, 13, 871873)),
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='START_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 25, 0, 52, 13, 871850)),
        ),
    ]
# Generated by Django 3.2.5 on 2021-08-21 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCQ', '0010_auto_20210807_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QSTN_ONE', models.CharField(max_length=200)),
                ('QSTN_ONE_ANSWR', models.CharField(max_length=50)),
                ('QSTN_TWO', models.CharField(max_length=200)),
                ('QSTN_TWO_ANSWR', models.CharField(max_length=50)),
                ('QSTN_THREE', models.CharField(max_length=200)),
                ('QSTN_THREE_ANSWR_CHOICE_1', models.CharField(max_length=850)),
                ('QSTN_THREE_ANSWR_CHOICE_2', models.CharField(blank=True, max_length=850)),
                ('QSTN_THREE_ANSWR_CHOICE_3', models.CharField(blank=True, max_length=850)),
                ('QSTN_THREE_ANSWR_CHOICE_4', models.CharField(blank=True, max_length=850)),
                ('COMMENTS', models.TextField(blank=True, max_length=5000)),
            ],
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='END_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 21, 12, 59, 43, 885855)),
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='START_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 21, 12, 59, 43, 885822)),
        ),
    ]
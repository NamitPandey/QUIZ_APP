# Generated by Django 3.2.5 on 2021-07-29 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCQ', '0008_auto_20210726_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizdata',
            name='PROGRAM',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizdata',
            name='SCHOOL',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='END_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 11, 58, 17, 813189)),
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='ENROLLMENT_NUMBER',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='enrollemntsforquiz',
            name='START_TIME',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 11, 58, 17, 813157)),
        ),
        migrations.AlterField(
            model_name='question',
            name='CATEGORY',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='question',
            name='CHOICE_1',
            field=models.CharField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='question',
            name='CHOICE_2',
            field=models.CharField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='question',
            name='CHOICE_3',
            field=models.CharField(blank=True, max_length=50000),
        ),
        migrations.AlterField(
            model_name='question',
            name='CHOICE_4',
            field=models.CharField(blank=True, max_length=50000),
        ),
        migrations.AlterField(
            model_name='question',
            name='CORRECT',
            field=models.CharField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='quizdata',
            name='ANSWER',
            field=models.CharField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='quizdata',
            name='CATEGORY',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='quizdata',
            name='CORRECT_ANSWER',
            field=models.CharField(max_length=50000),
        ),
    ]

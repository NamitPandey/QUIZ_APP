# Generated by Django 3.2.5 on 2021-07-17 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCQ', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizdata',
            name='END_TIME',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='quizdata',
            name='START_TIME',
            field=models.TimeField(auto_now=True),
        ),
    ]

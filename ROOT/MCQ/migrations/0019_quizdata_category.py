# Generated by Django 3.1.5 on 2021-02-26 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCQ', '0018_auto_20210226_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizdata',
            name='CATEGORY',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]

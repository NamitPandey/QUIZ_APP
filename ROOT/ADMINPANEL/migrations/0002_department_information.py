# Generated by Django 3.2.5 on 2021-08-23 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADMINPANEL', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NAME', models.CharField(max_length=254)),
                ('SCHOOL_NAME', models.CharField(max_length=254)),
                ('PROGRAM_NAME', models.CharField(max_length=254)),
                ('EMAIL_ID', models.EmailField(max_length=254)),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2021-06-05 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_studentsinfo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentsinfo',
            name='age',
        ),
    ]

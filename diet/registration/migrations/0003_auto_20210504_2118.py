# Generated by Django 3.1.7 on 2021-05-04 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20210504_2101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='temp',
        ),
        migrations.AlterField(
            model_name='register',
            name='age',
            field=models.BinaryField(max_length=500),
        ),
        migrations.AlterField(
            model_name='register',
            name='name',
            field=models.BinaryField(max_length=500),
        ),
    ]

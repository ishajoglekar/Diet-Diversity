# Generated by Django 3.2.4 on 2021-06-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_auto_20210607_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='studentsinfo',
            name='name',
            field=models.BinaryField(max_length=500),
        ),
    ]

# Generated by Django 3.2.3 on 2021-06-23 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0026_auto_20210622_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduleone',
            name='pre',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
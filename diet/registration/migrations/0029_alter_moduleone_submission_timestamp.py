# Generated by Django 3.2.3 on 2021-06-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0028_alter_moduleone_submission_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduleone',
            name='submission_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
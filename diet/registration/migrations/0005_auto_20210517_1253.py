# Generated by Django 3.1.7 on 2021-05-17 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20210507_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

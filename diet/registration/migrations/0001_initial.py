# Generated by Django 3.2 on 2021-05-04 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('facilities1', models.CharField(max_length=50)),
                ('facilities2', models.CharField(max_length=50)),
                ('facilities3', models.CharField(max_length=50)),
                ('sports', models.CharField(max_length=50)),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2021-06-05 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_auto_20210605_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('pincode', models.IntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.city')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.state')),
            ],
        ),
        migrations.CreateModel(
            name='StudentsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=255)),
                ('rollno', models.IntegerField()),
                ('gender', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.school')),
            ],
        ),
    ]
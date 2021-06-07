from os import name
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.
# class myValidate:
#     def validateGreaterThan0(value):
#         errors = []
#         if value:
#             if int(value) < 10:
#                 errors.append('Enter Age greater than 10')
#                 # raise ValidationError(
#                 #     'not an even number',
#                 #     params={'value': value},
#                 # )
#                 return errors

#     def validateRequired(value):
#         errors = []
#         print(value)
#         if isinstance(value,list):
#             if not value:
#                 errors.append('required field')
#                 return errors
#         elif not value.strip():
#             errors.append('required field')
#             print("Required Field")
#             return errors
       


class Occupation(models.Model):
    occupation = models.CharField(max_length=255)

    def __str__(self):
        return self.occupation

class State(models.Model):
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.state

class City(models.Model):
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.city

class FamilyType(models.Model):
    family = models.CharField(max_length=255)

    def __str__(self):
        return self.family

class ReligiousBelief(models.Model):
    religion = models.CharField(max_length=255)
    
    def __str__(self):
        return self.religion

class Education(models.Model):
    education = models.CharField(max_length=255)

    def __str__(self):
        return self.education
  
class ParentsInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    consent = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()
    occupation = models.ForeignKey(Occupation,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    edu = models.ForeignKey(Education,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    pincode = models.IntegerField()
    no_of_family_members = models.IntegerField()
    type_of_family = models.ForeignKey(FamilyType,on_delete=models.CASCADE)
    religion = models.ForeignKey(ReligiousBelief,on_delete=models.CASCADE)
    children_count = models.IntegerField()

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pincode = models.IntegerField()
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class StudentsInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    rollno = models.IntegerField()
    gender = models.CharField(max_length=255)
    dob = models.DateField()
    parent = models.ForeignKey(ParentsInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

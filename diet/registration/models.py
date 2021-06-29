from os import name
from datetime import date,timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from shared.encryption import EncryptionHelper
from django.core.validators import MinValueValidator, MaxValueValidator


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
    state = models.ForeignKey(State,on_delete=models.CASCADE,default=1)

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
  
class School(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    pincode = models.IntegerField()
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name


class ParentsInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.BinaryField(max_length=500)
    consent = models.BooleanField(default=True)
    name = models.BinaryField(max_length=500)
    gender = models.CharField(max_length=255)
    age = models.IntegerField(validators=[MinValueValidator(3)])
    occupation = models.ForeignKey(Occupation,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    edu = models.ForeignKey(Education,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    pincode = models.IntegerField()
    no_of_family_members = models.IntegerField()
    type_of_family = models.ForeignKey(FamilyType,on_delete=models.CASCADE)
    religion = models.ForeignKey(ReligiousBelief,on_delete=models.CASCADE)
    children_count = models.IntegerField(validators=[MinValueValidator(1)])
    first_password = models.CharField(max_length=20,default='helloworld14')
    password_changed = models.BooleanField(default=False)

    def __str__(self):
        encryptionHelper = EncryptionHelper()
        return encryptionHelper.decrypt(self.name)


class TeacherInCharge(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class StudentsInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.BinaryField(max_length=500)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    rollno = models.IntegerField(validators=[MinValueValidator(0)])
    gender = models.CharField(max_length=255)
    dob = models.DateField(validators=[MaxValueValidator(limit_value=date.today()-timedelta(days=(365*3)))])
    parent = models.ForeignKey(ParentsInfo,on_delete=models.CASCADE)
    first_password = models.CharField(max_length=20,default='helloworld14')
    password_changed = models.BooleanField(default=False)
    teacher = models.ForeignKey(TeacherInCharge,on_delete=models.CASCADE)

    def __str__(self):
        encryptionHelper = EncryptionHelper()
        return encryptionHelper.decrypt(self.name)


class FirstModule(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)  
    tennis = models.CharField(max_length=255)
    cricket = models.CharField(max_length=255)
    chess = models.CharField(max_length=255)
    food = models.CharField(max_length=255)
    drinks = models.CharField(max_length=255)

class Form(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name.capitalize()

class FormDetails(models.Model):
    form = models.ForeignKey(Form,on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherInCharge,on_delete=models.CASCADE)
    open = models.BooleanField()
    pre = models.BooleanField()
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField(null=True)


class ModuleOne(models.Model):
    student = models.ForeignKey(StudentsInfo,on_delete=models.CASCADE)
    pre = models.BooleanField()
    draft = models.BooleanField()
    nutriGarden = models.CharField(max_length=10,null=True)
    source_fruits_vegetables = models.CharField(max_length=255,null=True)
    grow_own_food = models.CharField(max_length=255,null=True)
    if_grow_what = models.CharField(max_length=255,null=True,default="NA")
    reason_gardening = models.CharField(max_length=255,null=True)
    healthy_diet = models.CharField(max_length=255,null=True)
    imp_nutrients = models.CharField(max_length=255,null=True)
    citrus_fruits_blank = models.CharField(max_length=255,null=True)
    not_richsource_iron = models.CharField(max_length=255,null=True)
    source_vitaminA = models.CharField(max_length=255,null=True)
    imp_eat_fruits_vegetables = models.CharField(max_length=255,null=True)
    reason_wide_variety_food = models.CharField(max_length=255,null=True)
    microgreen = models.CharField(max_length=255,null=True)
    microgreen_example = models.CharField(max_length=255,null=True)
    harvestdays_microgreen = models.CharField(max_length=255,null=True)
    microgreen_grow_seeds_kitchen = models.CharField(max_length=255,null=True)
    microgreen_nutritiousthan_fullgrownvegetables = models.CharField(max_length=255,null=True)
    microgreen_immunity = models.CharField(max_length=255,null=True)
    microgreen_variety = models.CharField(max_length=255,null=True)
    microgreen_source = models.CharField(max_length=255,null=True)
    newspaper_grow_microgreen = models.CharField(max_length=255,null=True)
    microgreen_first_step =  models.CharField(max_length=255,null=True)
    soaking_time_seeds =  models.CharField(max_length=255,null=True)
    microgreen_watering = models.CharField(max_length=255,null=True)
    microgreen_use =  models.CharField(max_length=255,null=True)
    submission_timestamp = models.DateTimeField(null=True)


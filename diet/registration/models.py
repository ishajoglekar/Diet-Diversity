from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from registration.models import *

# Create your models here.



class myValidate:
    def validateGreaterThan0(value):
        errors = []
        if value:
            if int(value) < 10:
                errors.append('Enter Age greater than 10')
                # raise ValidationError(
                #     'not an even number',
                #     params={'value': value},
                # )
                return errors

    def validateRequired(value):
        errors = []
        print(value)
        if isinstance(value,list):
            if not value:
                errors.append('required field')
                return errors
        elif not value.strip():
            errors.append('required field')
            print("Required Field")
            return errors

    
        

class Register(models.Model):
    name = models.BinaryField(max_length=500)
    age = models.BinaryField(max_length=500)
    height = models.IntegerField()
    weight = models.IntegerField()
    facilities1 = models.CharField(max_length=50)
    facilities2 = models.CharField(max_length=50)
    facilities3 = models.CharField(max_length=50)
    sports = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    password_changed = models.BooleanField()
    objects = myValidate()
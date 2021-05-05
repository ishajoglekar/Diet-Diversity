from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from registration.models import *

# Create your models here.



class myValidate:
    def validate(value):
        errors = []
        if int(value) % 2 != 0:
            errors.append('not an even number')
            print("Not an even number")
            # raise ValidationError(
            #     'not an even number',
            #     params={'value': value},
            # )
            return errors

    def validateRequired(value):
        errors = []
        if not value.strip():
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
    objects = myValidate()

    

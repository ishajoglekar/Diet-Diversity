from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.BinaryField(max_length=500)
    age = models.BinaryField(max_length=500)
    height = models.IntegerField()
    weight = models.IntegerField()
    facilities1 = models.CharField(max_length=50)
    facilities2 = models.CharField(max_length=50)
    facilities3 = models.CharField(max_length=50)
    sports = models.CharField(max_length=50)

    

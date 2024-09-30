from django.db import models
# Create your models here.
class GeneralInformation(models.Model):
    semester = models.IntegerField()
    year = models.CharField(max_length = 50)

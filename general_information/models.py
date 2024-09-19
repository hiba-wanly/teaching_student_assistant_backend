from django.db import models
# Create your models here.
class GeneralInformation(models.Model):
    semester = models.CharField(max_length = 50)
    year = models.CharField(max_length = 50)

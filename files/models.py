from django.db import models
from subject.models import Subject

# Create your models here.
class Files(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT)     
    name = models.CharField(max_length = 250)
    file_path = models.FileField(upload_to='uploadfiles/')
    published_date = models.CharField(max_length = 50)
    available_date = models.CharField(max_length = 50)
    type = models.CharField(max_length = 250)

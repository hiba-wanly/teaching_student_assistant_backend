from django.db import models
from student.models import Student
from subject.models import Subject
from files.models import Files
# Create your models here.
class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT)     
    homework_full_mark = models.FloatField()
    number_of_work = models.IntegerField()
    # type = models.CharField(max_length = 50)
    percentage = models.FloatField(null= True , blank=True)
    file = models.OneToOneField(Files, on_delete=models.CASCADE)

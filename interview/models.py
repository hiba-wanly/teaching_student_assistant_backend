from django.db import models
from student.models import Student
from subject.models import Subject

# Create your models here.
class Interview(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT)     
    # date = models.CharField(max_length = 50,null= True , blank=True)
    interview_full_mark = models.FloatField()
    number_of_interview = models.IntegerField()
    # type = models.CharField(max_length = 50)
    percentage = models.FloatField(null= True , blank=True)


     
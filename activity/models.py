from django.db import models
from student.models import Student
from subject.models import Subject

# Create your models here.
class Activity(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT)     
    # date = models.CharField(max_length = 50)
    activity_full_mark = models.FloatField()
    # type = models.CharField(max_length = 50)
    percentage = models.FloatField(null= True , blank=True)



class ActivityLOG(models.Model):
    activity = models.ForeignKey(Activity, on_delete = models.PROTECT)  
    student = models.ForeignKey(Student, on_delete = models.PROTECT)      
    mark = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT,null= True , blank=True) 
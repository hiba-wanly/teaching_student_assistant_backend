from django.db import models
from student.models import Student
from subject.models import Subject

# Create your models here.
class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT)     
    date = models.CharField(max_length = 50)
    day = models.CharField(max_length = 50)
    type = models.CharField(max_length = 50) # lab , theory
    percentage = models.FloatField(null= True , blank=True)



class AttendanceLOG(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete = models.PROTECT)  
    student = models.ForeignKey(Student, on_delete = models.PROTECT)      
    status = models.CharField(max_length = 50) # attended , absent , late , reason
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT,null= True , blank=True) 
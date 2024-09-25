from django.db import models
from departments.models import Departments

# Create your models here.
class Subject(models.Model):
    subject_name = models.CharField(max_length = 50)
    academic_year = models.CharField(max_length = 50)
    departments = models.ForeignKey(Departments, on_delete = models.PROTECT)
    semester = models.CharField(max_length = 50,null= True , blank=True)
    year = models.CharField(max_length = 50,null= True , blank=True)
    # major = models.CharField(max_length = 50,null= True , blank=True)
    tests_mark = models.IntegerField(null= True , blank=True)
    attendance_mark = models.IntegerField(null= True , blank=True)
    interviews_mark = models.IntegerField(null= True , blank=True)
    homework_mark = models.IntegerField(null= True , blank=True)
    labs_mark = models.IntegerField(null= True , blank=True)
    total_mark = models.IntegerField(null= True , blank=True)
    practical_mark = models.IntegerField(null= True , blank=True)
    # number_of_pracctical_sessions = models.IntegerField(null= True , blank=True)
    # number_of_theoretical_sessions = models.IntegerField(null= True , blank=True)
    # study_mark_from = models.IntegerField(null= True , blank=True)
    # work_mark_from = models.IntegerField(null= True , blank=True)
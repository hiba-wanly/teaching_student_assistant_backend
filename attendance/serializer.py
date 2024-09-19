from rest_framework import serializers
from .models import Attendance , AttendanceLOG

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        
        
class AttendanceLOGSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLOG
        fields = '__all__'
        

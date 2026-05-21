from rest_framework import serializers
from .models import *

class Employee_details(serializers.ModelSerializer):
    class Meta:
        model = employee_info
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
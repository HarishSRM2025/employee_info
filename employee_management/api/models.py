from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class employee_info(models.Model):
    tenant_id= models.CharField(null=False)
    employee_id=models.CharField(null=False)
    employee_name=models.CharField(null=False,max_length=100)
    employee_role=models.CharField(max_length=150,null=False)
    employee_salary=models.FloatField(null=False)
    employee_dob=models.DateField(null=False)
    employee_address=models.CharField(max_length=500,null=False)
    employee_phone_number=models.CharField(max_length=10,null=False)

    def __str__(self):
        return self.tenant_id+"_"+self.employee_name


def default_attendance_date():
    return timezone.now().date()


class Attendance(models.Model):
    tenant_id = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100)
    attendance_date = models.DateField(default=default_attendance_date)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=30, default='Present')
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-attendance_date', 'employee_name']

    def __str__(self):
        return f"{self.employee_name} - {self.attendance_date}"
# pyrefly: ignore [missing-import]
from django.db import models

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    LEAVE_TYPES = [
        ('LOP', 'Loss of Pay (LOP)'),
        ('Casual Leave', 'Casual Leave'),
        ('Weekoff', 'Weekoff'),
    ]

    tenant_id = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100)
    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee_name} - {self.leave_type} ({self.status})"

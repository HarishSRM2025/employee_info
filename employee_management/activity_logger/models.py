# pyrefly: ignore [missing-import]
from django.db import models

class ActivityLog(models.Model):
    tenant_id = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    activity_type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee_name} - {self.activity_type} ({self.status})"

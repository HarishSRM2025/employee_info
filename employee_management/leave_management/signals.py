from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest
from activity_logger.models import ActivityLog

@receiver(post_save, sender=LeaveRequest)
def log_leave_request_activity(sender, instance, created, **kwargs):
    if created:
        activity_type = "Leave Request Submitted"
        description = f"Requested {instance.leave_type} from {instance.start_date} to {instance.end_date}."
    else:
        activity_type = f"Leave Request {instance.status}"
        description = f"Leave request for {instance.leave_type} was {instance.status.lower()}."

    ActivityLog.objects.create(
        tenant_id=instance.tenant_id,
        employee_id=instance.employee_id,
        employee_name=instance.employee_name,
        activity_type=activity_type,
        description=description,
        status=instance.status
    )

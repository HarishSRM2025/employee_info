from rest_framework import viewsets
from .models import ActivityLog
from .serializers import ActivityLogSerializer

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        queryset = ActivityLog.objects.all()
        employee_id = self.request.query_params.get('employee_id', None)
        tenant_id = self.request.query_params.get('tenant_id', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if employee_id is not None:
            queryset = queryset.filter(employee_id=employee_id)
        if tenant_id is not None:
            queryset = queryset.filter(tenant_id=tenant_id)
        if activity_type is not None:
            queryset = queryset.filter(activity_type=activity_type)
            
        return queryset

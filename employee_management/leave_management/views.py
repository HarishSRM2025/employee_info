# pyrefly: ignore [missing-import]
from rest_framework import viewsets
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        queryset = LeaveRequest.objects.all()
        employee_id = self.request.query_params.get('employee_id', None)
        tenant_id = self.request.query_params.get('tenant_id', None)
        status = self.request.query_params.get('status', None)
        
        if employee_id is not None:
            queryset = queryset.filter(employee_id=employee_id)
        if tenant_id is not None:
            queryset = queryset.filter(tenant_id=tenant_id)
        if status is not None:
            queryset = queryset.filter(status=status)
            
        return queryset

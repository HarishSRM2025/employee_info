from django.urls import path
from . import views

urlpatterns = [
    path('tenant/employee_data/', views.employee_details),
    path('tenant/employee_data/<int:id>/', views.employee_data_with_id),
    path('tenant/attendance/', views.attendance_list),
    path('tenant/attendance/<int:id>/', views.attendance_detail),
    path('tenant/attendance/checkin/', views.attendance_checkin),
    path('tenant/attendance/checkout/', views.attendance_checkout),
]
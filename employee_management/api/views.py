from django.shortcuts import render
from django.utils import timezone
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['POST', 'GET', 'PUT'])
def employee_details(request):

    if request.method == 'POST':
        serializer = Employee_details(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Employee Data Uploaded Successfully",
                "data": serializer.data
            })
        return Response(serializer.errors)

    elif request.method == 'GET':
        employees_data = employee_info.objects.all()
        serializer = Employee_details(employees_data, many=True)
        return Response(serializer.data)

   
@api_view(['GET','PUT','DELETE'])
def employee_data_with_id(request, id):
    if request.method == 'GET': 
        try:
            employee = employee_info.objects.get(id=id)
            serializer = Employee_details(employee)
            return Response(serializer.data)
        except employee_info.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)
        

    elif request.method == 'PUT':
        try:
            employee = employee_info.objects.get(id=id)
        except employee_info.DoesNotExist:
            return Response({"error": "Employee not found"})

        serializer = Employee_details(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Employee Updated Successfully",
                "data": serializer.data
            })
        return Response(serializer.errors)    
    
    
    elif request.method == 'DELETE':
        try:
            employee = employee_info.objects.get(id=id)
            employee.delete()
            return Response({
                "Message": "Employee Deleted Successfully"
            })
        
        except employee_info.DoesNotExist:
            return Response({
                "error": "Employee not found"
            }, status=404)


@api_view(['GET', 'POST'])
def attendance_list(request):
    if request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Attendance record created successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=400)

    attendance_data = Attendance.objects.all()
    serializer = AttendanceSerializer(attendance_data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def attendance_detail(request, id):
    try:
        attendance = Attendance.objects.get(id=id)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found"}, status=404)

    if request.method == 'GET':
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Attendance record updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        attendance.delete()
        return Response({"Message": "Attendance record deleted successfully"})


@api_view(['POST'])
def attendance_checkin(request):
    employee_id = request.data.get('employee_id')
    tenant_id = request.data.get('tenant_id')
    employee_name = request.data.get('employee_name', '')
    attendance_date = request.data.get('attendance_date')
    check_in_time = request.data.get('check_in_time')

    if not employee_id or not tenant_id:
        return Response({"error": "employee_id and tenant_id are required"}, status=400)

    if attendance_date:
        try:
            attendance_date = datetime.date.fromisoformat(attendance_date)
        except ValueError:
            return Response({"error": "attendance_date must be in YYYY-MM-DD format"}, status=400)
    else:
        attendance_date = timezone.localdate()

    if check_in_time:
        try:
            check_in_time = datetime.time.fromisoformat(check_in_time)
        except ValueError:
            return Response({"error": "check_in_time must be in HH:MM[:SS] format"}, status=400)
    else:
        check_in_time = timezone.localtime().time()

    attendance, created = Attendance.objects.get_or_create(
        tenant_id=tenant_id,
        employee_id=employee_id,
        attendance_date=attendance_date,
        defaults={
            'employee_name': employee_name,
            'check_in_time': check_in_time,
            'status': 'Present'
        }
    )

    if not created and attendance.check_in_time:
        return Response({"error": "Employee already checked in for today"}, status=400)

    attendance.employee_name = employee_name or attendance.employee_name
    attendance.check_in_time = check_in_time
    attendance.status = 'Present'
    attendance.save()

    serializer = AttendanceSerializer(attendance)
    return Response({"Message": "Check-in recorded successfully", "data": serializer.data})


@api_view(['POST'])
def attendance_checkout(request):
    employee_id = request.data.get('employee_id')
    tenant_id = request.data.get('tenant_id')
    attendance_date = request.data.get('attendance_date')
    check_out_time = request.data.get('check_out_time')

    if not employee_id or not tenant_id:
        return Response({"error": "employee_id and tenant_id are required"}, status=400)

    if attendance_date:
        try:
            attendance_date = datetime.date.fromisoformat(attendance_date)
        except ValueError:
            return Response({"error": "attendance_date must be in YYYY-MM-DD format"}, status=400)
    else:
        attendance_date = timezone.localdate()

    if check_out_time:
        try:
            check_out_time = datetime.time.fromisoformat(check_out_time)
        except ValueError:
            return Response({"error": "check_out_time must be in HH:MM[:SS] format"}, status=400)
    else:
        check_out_time = timezone.localtime().time()

    try:
        attendance = Attendance.objects.get(
            tenant_id=tenant_id,
            employee_id=employee_id,
            attendance_date=attendance_date
        )
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found for this employee and date"}, status=404)

    attendance.check_out_time = check_out_time
    if not attendance.check_in_time:
        attendance.status = 'Absent'
    attendance.save()

    serializer = AttendanceSerializer(attendance)
    return Response({"Message": "Check-out recorded successfully", "data": serializer.data})
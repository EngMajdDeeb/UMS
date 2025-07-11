from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Department, Student, StudentAcademicRecord
from .serializers import DepartmentSerializer, StudentSerializer, StudentAcademicRecordSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students in a department"""
        department = self.get_object()
        students = Student.objects.filter(department=department)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get department statistics"""
        department = self.get_object()
        stats = {
            'total_students': Student.objects.filter(department=department).count(),
            'active_students': Student.objects.filter(department=department, status='active').count(),
            'average_gpa': Student.objects.filter(department=department).aggregate(avg_gpa=Avg('gpa'))['avg_gpa'] or 0,
            'students_by_level': list(Student.objects.filter(department=department).values('academic_level').annotate(count=Count('id')))
        }
        return Response(stats)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Student.objects.all()
        department = self.request.query_params.get('department')
        status = self.request.query_params.get('status')
        academic_level = self.request.query_params.get('academic_level')
        
        if department:
            queryset = queryset.filter(department_id=department)
        if status:
            queryset = queryset.filter(status=status)
        if academic_level:
            queryset = queryset.filter(academic_level=academic_level)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def academic_records(self, request, pk=None):
        """Get student's academic records"""
        student = self.get_object()
        records = StudentAcademicRecord.objects.filter(student=student).order_by('-year', '-semester')
        serializer = StudentAcademicRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update student status"""
        student = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Student.STATUS_CHOICES):
            student.status = new_status
            student.save()
            return Response({'status': 'success', 'new_status': new_status})
        return Response({'error': 'Invalid status'}, status=400)


class StudentAcademicRecordViewSet(viewsets.ModelViewSet):
    queryset = StudentAcademicRecord.objects.all()
    serializer_class = StudentAcademicRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = StudentAcademicRecord.objects.all()
        student = self.request.query_params.get('student')
        year = self.request.query_params.get('year')
        
        if student:
            queryset = queryset.filter(student_id=student)
        if year:
            queryset = queryset.filter(year=year)
            
        return queryset.order_by('-year', '-semester')
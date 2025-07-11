from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Faculty, FacultyQualification, FacultyLeave
from .serializers import FacultySerializer, FacultyQualificationSerializer, FacultyLeaveSerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Faculty.objects.all()
        department = self.request.query_params.get('department')
        position = self.request.query_params.get('position')
        status = self.request.query_params.get('status')
        
        if department:
            queryset = queryset.filter(department_id=department)
        if position:
            queryset = queryset.filter(position=position)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def qualifications(self, request, pk=None):
        """Get faculty qualifications"""
        faculty = self.get_object()
        qualifications = FacultyQualification.objects.filter(faculty=faculty)
        serializer = FacultyQualificationSerializer(qualifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def leaves(self, request, pk=None):
        """Get faculty leaves"""
        faculty = self.get_object()
        leaves = FacultyLeave.objects.filter(faculty=faculty).order_by('-applied_on')
        serializer = FacultyLeaveSerializer(leaves, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get faculty statistics"""
        stats = {
            'total_faculty': Faculty.objects.count(),
            'active_faculty': Faculty.objects.filter(status='active').count(),
            'faculty_by_position': list(Faculty.objects.values('position').annotate(count=Count('id'))),
            'faculty_by_department': list(Faculty.objects.values('department__name').annotate(count=Count('id'))),
            'average_experience': Faculty.objects.aggregate(avg_exp=Avg('experience_years'))['avg_exp'] or 0
        }
        return Response(stats)


class FacultyQualificationViewSet(viewsets.ModelViewSet):
    queryset = FacultyQualification.objects.all()
    serializer_class = FacultyQualificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = FacultyQualification.objects.all()
        faculty = self.request.query_params.get('faculty')
        degree_type = self.request.query_params.get('degree_type')
        
        if faculty:
            queryset = queryset.filter(faculty_id=faculty)
        if degree_type:
            queryset = queryset.filter(degree_type=degree_type)
            
        return queryset


class FacultyLeaveViewSet(viewsets.ModelViewSet):
    queryset = FacultyLeave.objects.all()
    serializer_class = FacultyLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = FacultyLeave.objects.all()
        faculty = self.request.query_params.get('faculty')
        status = self.request.query_params.get('status')
        leave_type = self.request.query_params.get('leave_type')
        
        if faculty:
            queryset = queryset.filter(faculty_id=faculty)
        if status:
            queryset = queryset.filter(status=status)
        if leave_type:
            queryset = queryset.filter(leave_type=leave_type)
            
        return queryset.order_by('-applied_on')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a leave application"""
        leave = self.get_object()
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.approved_on = timezone.now()
        leave.save()
        return Response({'status': 'success', 'message': 'Leave approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a leave application"""
        leave = self.get_object()
        leave.status = 'rejected'
        leave.approved_by = request.user
        leave.approved_on = timezone.now()
        leave.remarks = request.data.get('remarks', '')
        leave.save()
        return Response({'status': 'success', 'message': 'Leave rejected'})
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.utils import timezone
from .models import Course, CourseOffering, StudentEnrollment, Assignment, StudentAssignment
from .serializers import (CourseSerializer, CourseOfferingSerializer, StudentEnrollmentSerializer,
                         AssignmentSerializer, StudentAssignmentSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Course.objects.all()
        department = self.request.query_params.get('department')
        course_type = self.request.query_params.get('course_type')
        is_active = self.request.query_params.get('is_active')
        
        if department:
            queryset = queryset.filter(department_id=department)
        if course_type:
            queryset = queryset.filter(course_type=course_type)
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def offerings(self, request, pk=None):
        """Get course offerings"""
        course = self.get_object()
        offerings = CourseOffering.objects.filter(course=course)
        serializer = CourseOfferingSerializer(offerings, many=True)
        return Response(serializer.data)


class CourseOfferingViewSet(viewsets.ModelViewSet):
    queryset = CourseOffering.objects.all()
    serializer_class = CourseOfferingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = CourseOffering.objects.all()
        semester = self.request.query_params.get('semester')
        year = self.request.query_params.get('year')
        instructor = self.request.query_params.get('instructor')
        
        if semester:
            queryset = queryset.filter(semester=semester)
        if year:
            queryset = queryset.filter(year=year)
        if instructor:
            queryset = queryset.filter(instructor_id=instructor)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get course enrollments"""
        offering = self.get_object()
        enrollments = StudentEnrollment.objects.filter(course_offering=offering)
        serializer = StudentEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get course assignments"""
        offering = self.get_object()
        assignments = Assignment.objects.filter(course_offering=offering)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = StudentEnrollment.objects.all()
        student = self.request.query_params.get('student')
        course_offering = self.request.query_params.get('course_offering')
        status = self.request.query_params.get('status')
        
        if student:
            queryset = queryset.filter(student_id=student)
        if course_offering:
            queryset = queryset.filter(course_offering_id=course_offering)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Assignment.objects.all()
        course_offering = self.request.query_params.get('course_offering')
        assignment_type = self.request.query_params.get('assignment_type')
        
        if course_offering:
            queryset = queryset.filter(course_offering_id=course_offering)
        if assignment_type:
            queryset = queryset.filter(assignment_type=assignment_type)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get assignment submissions"""
        assignment = self.get_object()
        submissions = StudentAssignment.objects.filter(assignment=assignment)
        serializer = StudentAssignmentSerializer(submissions, many=True)
        return Response(serializer.data)


class StudentAssignmentViewSet(viewsets.ModelViewSet):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = StudentAssignment.objects.all()
        student = self.request.query_params.get('student')
        assignment = self.request.query_params.get('assignment')
        status = self.request.query_params.get('status')
        
        if student:
            queryset = queryset.filter(student_id=student)
        if assignment:
            queryset = queryset.filter(assignment_id=assignment)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """Grade an assignment"""
        submission = self.get_object()
        marks = request.data.get('marks_obtained')
        feedback = request.data.get('feedback', '')
        
        if marks is not None:
            submission.marks_obtained = marks
            submission.feedback = feedback
            submission.status = 'graded'
            submission.graded_by = request.user
            submission.graded_on = timezone.now()
            submission.save()
            return Response({'status': 'success', 'message': 'Assignment graded'})
        return Response({'error': 'Marks required'}, status=400)
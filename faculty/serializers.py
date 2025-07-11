from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Faculty, FacultyQualification, FacultyLeave


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class FacultySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = ['id', 'user', 'faculty_id', 'department', 'department_name', 'first_name', 
                 'last_name', 'middle_name', 'full_name', 'date_of_birth', 'gender', 'phone', 
                 'email', 'address', 'position', 'hire_date', 'office_location', 'office_phone',
                 'specialization', 'education_qualifications', 'experience_years', 'salary', 
                 'status', 'research_interests', 'publications', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class FacultyQualificationSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.first_name', read_only=True)
    faculty_id = serializers.CharField(source='faculty.faculty_id', read_only=True)
    
    class Meta:
        model = FacultyQualification
        fields = ['id', 'faculty', 'faculty_name', 'faculty_id', 'degree_type', 'degree_name',
                 'institution', 'year_obtained', 'specialization', 'grade', 'created_at']
        read_only_fields = ['id', 'created_at']


class FacultyLeaveSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.first_name', read_only=True)
    faculty_id = serializers.CharField(source='faculty.faculty_id', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.first_name', read_only=True)
    
    class Meta:
        model = FacultyLeave
        fields = ['id', 'faculty', 'faculty_name', 'faculty_id', 'leave_type', 'start_date',
                 'end_date', 'reason', 'status', 'applied_on', 'approved_by', 'approved_by_name',
                 'approved_on', 'remarks']
        read_only_fields = ['id', 'applied_on']
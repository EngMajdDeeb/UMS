from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Student, StudentAcademicRecord


class DepartmentSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'student_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_student_count(self, obj):
        return obj.student_set.count()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'department', 'department_name', 'first_name', 
                 'last_name', 'middle_name', 'full_name', 'date_of_birth', 'gender', 'phone', 
                 'email', 'address', 'academic_level', 'enrollment_date', 'expected_graduation_date',
                 'current_semester', 'gpa', 'status', 'emergency_contact_name', 
                 'emergency_contact_phone', 'emergency_contact_relationship', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class StudentAcademicRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    
    class Meta:
        model = StudentAcademicRecord
        fields = ['id', 'student', 'student_name', 'student_id', 'semester', 'year', 
                 'semester_gpa', 'cumulative_gpa', 'credits_earned', 'total_credits',
                 'academic_standing', 'created_at']
        read_only_fields = ['id', 'created_at']
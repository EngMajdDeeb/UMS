from rest_framework import serializers
from .models import Course, CourseOffering, StudentEnrollment, Assignment, StudentAssignment


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_name', 'department', 'department_name', 'course_type',
                 'credit_hours', 'contact_hours', 'description', 'prerequisites', 'syllabus',
                 'learning_objectives', 'assessment_methods', 'textbooks', 'reference_books',
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseOfferingSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    course_name = serializers.CharField(source='course.course_name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.first_name', read_only=True)
    enrollment_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseOffering
        fields = ['id', 'course', 'course_code', 'course_name', 'instructor', 'instructor_name',
                 'semester', 'year', 'section', 'max_enrollment', 'current_enrollment',
                 'enrollment_percentage', 'classroom', 'schedule', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_enrollment_percentage(self, obj):
        if obj.max_enrollment > 0:
            return round((obj.current_enrollment / obj.max_enrollment) * 100, 2)
        return 0


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    course_code = serializers.CharField(source='course_offering.course.course_code', read_only=True)
    course_name = serializers.CharField(source='course_offering.course.course_name', read_only=True)
    
    class Meta:
        model = StudentEnrollment
        fields = ['id', 'student', 'student_name', 'student_id', 'course_offering', 'course_code',
                 'course_name', 'enrollment_date', 'status', 'final_grade', 'grade_points',
                 'attendance_percentage']
        read_only_fields = ['id', 'enrollment_date']


class AssignmentSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course_offering.course.course_code', read_only=True)
    course_name = serializers.CharField(source='course_offering.course.course_name', read_only=True)
    
    class Meta:
        model = Assignment
        fields = ['id', 'course_offering', 'course_code', 'course_name', 'title', 'description',
                 'assignment_type', 'total_marks', 'weight_percentage', 'due_date', 'is_active',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    graded_by_name = serializers.CharField(source='graded_by.first_name', read_only=True)
    
    class Meta:
        model = StudentAssignment
        fields = ['id', 'student', 'student_name', 'student_id', 'assignment', 'assignment_title',
                 'submission_date', 'submission_file', 'submission_text', 'marks_obtained',
                 'feedback', 'status', 'graded_by', 'graded_by_name', 'graded_on']
        read_only_fields = ['id', 'graded_on']
from django.contrib import admin
from .models import Course, CourseOffering, StudentEnrollment, Assignment, StudentAssignment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department', 'course_type', 'credit_hours', 'is_active')
    list_filter = ('department', 'course_type', 'is_active')
    search_fields = ('course_code', 'course_name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('prerequisites',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course_code', 'course_name', 'department', 'course_type', 'credit_hours', 'contact_hours', 'is_active')
        }),
        ('Course Details', {
            'fields': ('description', 'prerequisites', 'syllabus', 'learning_objectives', 'assessment_methods')
        }),
        ('Resources', {
            'fields': ('textbooks', 'reference_books')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course', 'instructor', 'semester', 'year', 'section', 'current_enrollment', 'max_enrollment', 'is_active')
    list_filter = ('semester', 'year', 'is_active')
    search_fields = ('course__course_code', 'course__course_name', 'instructor__faculty_id')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_offering', 'status', 'final_grade', 'enrollment_date')
    list_filter = ('status', 'enrollment_date', 'course_offering__semester', 'course_offering__year')
    search_fields = ('student__student_id', 'course_offering__course__course_code')
    readonly_fields = ('id', 'enrollment_date')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('course_offering', 'title', 'assignment_type', 'total_marks', 'due_date', 'is_active')
    list_filter = ('assignment_type', 'due_date', 'is_active')
    search_fields = ('title', 'course_offering__course__course_code')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'marks_obtained', 'submission_date', 'graded_on')
    list_filter = ('status', 'submission_date', 'graded_on')
    search_fields = ('student__student_id', 'assignment__title')
    readonly_fields = ('id', 'graded_on')
    
    fieldsets = (
        ('Assignment Information', {
            'fields': ('student', 'assignment', 'submission_date', 'status')
        }),
        ('Submission', {
            'fields': ('submission_file', 'submission_text')
        }),
        ('Grading', {
            'fields': ('marks_obtained', 'feedback', 'graded_by', 'graded_on')
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        })
    )
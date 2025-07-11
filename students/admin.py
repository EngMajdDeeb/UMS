from django.contrib import admin
from .models import Department, Student, StudentAcademicRecord


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'department', 'academic_level', 'status')
    list_filter = ('department', 'academic_level', 'status', 'gender')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'student_id', 'department')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender', 'phone', 'email', 'address')
        }),
        ('Academic Information', {
            'fields': ('academic_level', 'enrollment_date', 'expected_graduation_date', 'current_semester', 'gpa', 'status')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(StudentAcademicRecord)
class StudentAcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'year', 'semester', 'semester_gpa', 'cumulative_gpa', 'academic_standing')
    list_filter = ('year', 'semester', 'academic_standing')
    search_fields = ('student__student_id', 'student__first_name', 'student__last_name')
    readonly_fields = ('id', 'created_at')
from django.contrib import admin
from .models import Faculty, FacultyQualification, FacultyLeave


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'first_name', 'last_name', 'department', 'position', 'status')
    list_filter = ('department', 'position', 'status', 'gender')
    search_fields = ('faculty_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'faculty_id', 'department')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender', 'phone', 'email', 'address')
        }),
        ('Professional Information', {
            'fields': ('position', 'hire_date', 'office_location', 'office_phone', 'specialization', 'qualifications', 'experience_years', 'salary', 'status')
        }),
        ('Academic Information', {
            'fields': ('research_interests', 'publications')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(FacultyQualification)
class FacultyQualificationAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'degree_type', 'degree_name', 'institution', 'year_obtained')
    list_filter = ('degree_type', 'year_obtained')
    search_fields = ('faculty__faculty_id', 'faculty__first_name', 'faculty__last_name', 'degree_name', 'institution')
    readonly_fields = ('id', 'created_at')


@admin.register(FacultyLeave)
class FacultyLeaveAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'leave_type', 'start_date', 'end_date', 'status', 'applied_on')
    list_filter = ('leave_type', 'status', 'applied_on')
    search_fields = ('faculty__faculty_id', 'faculty__first_name', 'faculty__last_name')
    readonly_fields = ('id', 'applied_on')
    
    fieldsets = (
        ('Leave Information', {
            'fields': ('faculty', 'leave_type', 'start_date', 'end_date', 'reason')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'approved_on', 'remarks')
        }),
        ('Metadata', {
            'fields': ('id', 'applied_on'),
            'classes': ('collapse',)
        })
    )
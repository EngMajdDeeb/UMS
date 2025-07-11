from django.contrib import admin
from .models import Dean, DeanshipDecision, DeanshipMeeting, DepartmentBudget, DeanshipReport


@admin.register(Dean)
class DeanAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'department', 'appointed_date', 'status')
    list_filter = ('status', 'appointed_date', 'department')
    search_fields = ('faculty__faculty_id', 'faculty__first_name', 'faculty__last_name', 'department__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('faculty', 'department', 'appointed_date', 'term_end_date', 'status')
        }),
        ('Details', {
            'fields': ('responsibilities',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DeanshipDecision)
class DeanshipDecisionAdmin(admin.ModelAdmin):
    list_display = ('dean', 'title', 'decision_type', 'status', 'decision_date')
    list_filter = ('decision_type', 'status', 'decision_date')
    search_fields = ('title', 'description', 'dean__faculty__first_name', 'dean__faculty__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Decision Information', {
            'fields': ('dean', 'decision_type', 'title', 'description', 'decision_date', 'status')
        }),
        ('Implementation', {
            'fields': ('implementation_date', 'affected_parties', 'budget_impact')
        }),
        ('Documentation', {
            'fields': ('documents', 'remarks')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DeanshipMeeting)
class DeanshipMeetingAdmin(admin.ModelAdmin):
    list_display = ('dean', 'title', 'meeting_type', 'meeting_date', 'location', 'status')
    list_filter = ('meeting_type', 'status', 'meeting_date')
    search_fields = ('title', 'description', 'dean__faculty__first_name', 'dean__faculty__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('attendees',)
    
    fieldsets = (
        ('Meeting Information', {
            'fields': ('dean', 'meeting_type', 'title', 'description', 'meeting_date', 'location', 'status')
        }),
        ('Agenda & Attendees', {
            'fields': ('agenda', 'attendees')
        }),
        ('Meeting Minutes', {
            'fields': ('minutes', 'action_items', 'documents')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DepartmentBudget)
class DepartmentBudgetAdmin(admin.ModelAdmin):
    list_display = ('dean', 'title', 'budget_type', 'fiscal_year', 'requested_amount', 'approved_amount', 'status')
    list_filter = ('budget_type', 'fiscal_year', 'status')
    search_fields = ('title', 'description', 'dean__faculty__first_name', 'dean__faculty__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Budget Information', {
            'fields': ('dean', 'budget_type', 'fiscal_year', 'title', 'description', 'status')
        }),
        ('Financial Details', {
            'fields': ('requested_amount', 'approved_amount', 'spent_amount', 'justification')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_date', 'supporting_documents')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DeanshipReport)
class DeanshipReportAdmin(admin.ModelAdmin):
    list_display = ('dean', 'title', 'report_type', 'report_period', 'submission_date')
    list_filter = ('report_type', 'submission_date')
    search_fields = ('title', 'content', 'dean__faculty__first_name', 'dean__faculty__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('dean', 'report_type', 'title', 'report_period', 'submitted_to', 'submission_date')
        }),
        ('Content', {
            'fields': ('content', 'statistics', 'achievements', 'challenges', 'recommendations')
        }),
        ('Attachments', {
            'fields': ('attachments',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dean, DeanshipDecision, DeanshipMeeting, DepartmentBudget, DeanshipReport


class DeanSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.first_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Dean
        fields = ['id', 'faculty', 'faculty_name', 'department', 'department_name', 'appointed_date',
                 'term_end_date', 'status', 'responsibilities', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeanshipDecisionSerializer(serializers.ModelSerializer):
    dean_name = serializers.CharField(source='dean.faculty.first_name', read_only=True)
    department_name = serializers.CharField(source='dean.department.name', read_only=True)
    
    class Meta:
        model = DeanshipDecision
        fields = ['id', 'dean', 'dean_name', 'department_name', 'decision_type', 'title',
                 'description', 'decision_date', 'status', 'implementation_date',
                 'affected_parties', 'budget_impact', 'documents', 'remarks',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeanshipMeetingSerializer(serializers.ModelSerializer):
    dean_name = serializers.CharField(source='dean.faculty.first_name', read_only=True)
    department_name = serializers.CharField(source='dean.department.name', read_only=True)
    
    class Meta:
        model = DeanshipMeeting
        fields = ['id', 'dean', 'dean_name', 'department_name', 'meeting_type', 'title',
                 'description', 'meeting_date', 'location', 'agenda', 'attendees',
                 'status', 'minutes', 'action_items', 'documents', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DepartmentBudgetSerializer(serializers.ModelSerializer):
    dean_name = serializers.CharField(source='dean.faculty.first_name', read_only=True)
    department_name = serializers.CharField(source='dean.department.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.first_name', read_only=True)
    remaining_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = DepartmentBudget
        fields = ['id', 'dean', 'dean_name', 'department_name', 'budget_type', 'fiscal_year',
                 'title', 'description', 'requested_amount', 'approved_amount', 'spent_amount',
                 'remaining_amount', 'status', 'justification', 'supporting_documents',
                 'approved_by', 'approved_by_name', 'approved_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_remaining_amount(self, obj):
        if obj.approved_amount:
            return obj.approved_amount - obj.spent_amount
        return 0


class DeanshipReportSerializer(serializers.ModelSerializer):
    dean_name = serializers.CharField(source='dean.faculty.first_name', read_only=True)
    department_name = serializers.CharField(source='dean.department.name', read_only=True)
    
    class Meta:
        model = DeanshipReport
        fields = ['id', 'dean', 'dean_name', 'department_name', 'report_type', 'title',
                 'report_period', 'content', 'statistics', 'achievements', 'challenges',
                 'recommendations', 'attachments', 'submitted_to', 'submission_date',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Dean, DeanshipDecision, DeanshipMeeting, DepartmentBudget, DeanshipReport
from .serializers import (DeanSerializer, DeanshipDecisionSerializer, DeanshipMeetingSerializer,
                         DepartmentBudgetSerializer, DeanshipReportSerializer)


class DeanViewSet(viewsets.ModelViewSet):
    queryset = Dean.objects.all()
    serializer_class = DeanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Dean.objects.all()
        department = self.request.query_params.get('department')
        status = self.request.query_params.get('status')
        
        if department:
            queryset = queryset.filter(department_id=department)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def decisions(self, request, pk=None):
        """Get dean's decisions"""
        dean = self.get_object()
        decisions = DeanshipDecision.objects.filter(dean=dean).order_by('-decision_date')
        serializer = DeanshipDecisionSerializer(decisions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def meetings(self, request, pk=None):
        """Get dean's meetings"""
        dean = self.get_object()
        meetings = DeanshipMeeting.objects.filter(dean=dean).order_by('-meeting_date')
        serializer = DeanshipMeetingSerializer(meetings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def budgets(self, request, pk=None):
        """Get department budgets"""
        dean = self.get_object()
        budgets = DepartmentBudget.objects.filter(dean=dean).order_by('-fiscal_year')
        serializer = DepartmentBudgetSerializer(budgets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Get dean dashboard statistics"""
        dean = self.get_object()
        stats = {
            'total_decisions': DeanshipDecision.objects.filter(dean=dean).count(),
            'pending_decisions': DeanshipDecision.objects.filter(dean=dean, status='pending').count(),
            'upcoming_meetings': DeanshipMeeting.objects.filter(dean=dean, meeting_date__gte=timezone.now()).count(),
            'total_budget': DepartmentBudget.objects.filter(dean=dean, status='approved').aggregate(total=Sum('approved_amount'))['total'] or 0,
            'spent_budget': DepartmentBudget.objects.filter(dean=dean, status='approved').aggregate(spent=Sum('spent_amount'))['spent'] or 0,
        }
        return Response(stats)


class DeanshipDecisionViewSet(viewsets.ModelViewSet):
    queryset = DeanshipDecision.objects.all()
    serializer_class = DeanshipDecisionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = DeanshipDecision.objects.all()
        dean = self.request.query_params.get('dean')
        decision_type = self.request.query_params.get('decision_type')
        status = self.request.query_params.get('status')
        
        if dean:
            queryset = queryset.filter(dean_id=dean)
        if decision_type:
            queryset = queryset.filter(decision_type=decision_type)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('-decision_date')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a decision"""
        decision = self.get_object()
        decision.status = 'approved'
        decision.save()
        return Response({'status': 'success', 'message': 'Decision approved'})
    
    @action(detail=True, methods=['post'])
    def implement(self, request, pk=None):
        """Mark decision as implemented"""
        decision = self.get_object()
        decision.status = 'implemented'
        decision.implementation_date = timezone.now()
        decision.save()
        return Response({'status': 'success', 'message': 'Decision marked as implemented'})


class DeanshipMeetingViewSet(viewsets.ModelViewSet):
    queryset = DeanshipMeeting.objects.all()
    serializer_class = DeanshipMeetingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = DeanshipMeeting.objects.all()
        dean = self.request.query_params.get('dean')
        meeting_type = self.request.query_params.get('meeting_type')
        status = self.request.query_params.get('status')
        
        if dean:
            queryset = queryset.filter(dean_id=dean)
        if meeting_type:
            queryset = queryset.filter(meeting_type=meeting_type)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('-meeting_date')
    
    @action(detail=True, methods=['post'])
    def start_meeting(self, request, pk=None):
        """Start a meeting"""
        meeting = self.get_object()
        meeting.status = 'in_progress'
        meeting.save()
        return Response({'status': 'success', 'message': 'Meeting started'})
    
    @action(detail=True, methods=['post'])
    def complete_meeting(self, request, pk=None):
        """Complete a meeting"""
        meeting = self.get_object()
        meeting.status = 'completed'
        meeting.minutes = request.data.get('minutes', '')
        meeting.action_items = request.data.get('action_items', '')
        meeting.save()
        return Response({'status': 'success', 'message': 'Meeting completed'})


class DepartmentBudgetViewSet(viewsets.ModelViewSet):
    queryset = DepartmentBudget.objects.all()
    serializer_class = DepartmentBudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = DepartmentBudget.objects.all()
        dean = self.request.query_params.get('dean')
        budget_type = self.request.query_params.get('budget_type')
        fiscal_year = self.request.query_params.get('fiscal_year')
        status = self.request.query_params.get('status')
        
        if dean:
            queryset = queryset.filter(dean_id=dean)
        if budget_type:
            queryset = queryset.filter(budget_type=budget_type)
        if fiscal_year:
            queryset = queryset.filter(fiscal_year=fiscal_year)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('-fiscal_year')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a budget"""
        budget = self.get_object()
        approved_amount = request.data.get('approved_amount')
        if approved_amount:
            budget.approved_amount = approved_amount
            budget.status = 'approved'
            budget.approved_by = request.user
            budget.approved_date = timezone.now()
            budget.save()
            return Response({'status': 'success', 'message': 'Budget approved'})
        return Response({'error': 'Approved amount required'}, status=400)


class DeanshipReportViewSet(viewsets.ModelViewSet):
    queryset = DeanshipReport.objects.all()
    serializer_class = DeanshipReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = DeanshipReport.objects.all()
        dean = self.request.query_params.get('dean')
        report_type = self.request.query_params.get('report_type')
        
        if dean:
            queryset = queryset.filter(dean_id=dean)
        if report_type:
            queryset = queryset.filter(report_type=report_type)
            
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a report"""
        report = self.get_object()
        report.submitted_to = request.data.get('submitted_to', '')
        report.submission_date = timezone.now()
        report.save()
        return Response({'status': 'success', 'message': 'Report submitted'})
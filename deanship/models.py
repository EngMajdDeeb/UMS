from django.db import models
from django.contrib.auth.models import User
import uuid


class Dean(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.OneToOneField('faculty.Faculty', on_delete=models.CASCADE)
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE)
    appointed_date = models.DateField()
    term_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    responsibilities = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dean {self.faculty.first_name} {self.faculty.last_name} - {self.department.name}"
    
    class Meta:
        verbose_name = 'Dean'
        verbose_name_plural = 'Deans'


class DeanshipDecision(models.Model):
    DECISION_TYPES = [
        ('policy', 'Policy Decision'),
        ('academic', 'Academic Decision'),
        ('disciplinary', 'Disciplinary Action'),
        ('budget', 'Budget Decision'),
        ('faculty_hiring', 'Faculty Hiring'),
        ('course_approval', 'Course Approval'),
        ('student_appeal', 'Student Appeal'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
        ('implemented', 'Implemented'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dean = models.ForeignKey(Dean, on_delete=models.CASCADE)
    decision_type = models.CharField(max_length=20, choices=DECISION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    decision_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    implementation_date = models.DateTimeField(null=True, blank=True)
    affected_parties = models.TextField(blank=True)
    budget_impact = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    documents = models.FileField(upload_to='deanship/decisions/', null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.dean.department.name} - {self.title}"
    
    class Meta:
        verbose_name = 'Deanship Decision'
        verbose_name_plural = 'Deanship Decisions'
        ordering = ['-decision_date']


class DeanshipMeeting(models.Model):
    MEETING_TYPES = [
        ('department', 'Department Meeting'),
        ('faculty', 'Faculty Meeting'),
        ('academic_council', 'Academic Council'),
        ('administrative', 'Administrative Meeting'),
        ('disciplinary', 'Disciplinary Committee'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dean = models.ForeignKey(Dean, on_delete=models.CASCADE)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    meeting_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    agenda = models.TextField()
    attendees = models.ManyToManyField(User, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    minutes = models.TextField(blank=True)
    action_items = models.TextField(blank=True)
    documents = models.FileField(upload_to='deanship/meetings/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.meeting_type} - {self.title} ({self.meeting_date.strftime('%Y-%m-%d')})"
    
    class Meta:
        verbose_name = 'Deanship Meeting'
        verbose_name_plural = 'Deanship Meetings'
        ordering = ['-meeting_date']


class DepartmentBudget(models.Model):
    BUDGET_TYPES = [
        ('operational', 'Operational Budget'),
        ('capital', 'Capital Expenditure'),
        ('research', 'Research Budget'),
        ('infrastructure', 'Infrastructure Budget'),
        ('staff', 'Staff Budget'),
        ('student_activities', 'Student Activities Budget'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dean = models.ForeignKey(Dean, on_delete=models.CASCADE)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES)
    fiscal_year = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    justification = models.TextField()
    supporting_documents = models.FileField(upload_to='deanship/budgets/', null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.dean.department.name} - {self.title} ({self.fiscal_year})"
    
    class Meta:
        verbose_name = 'Department Budget'
        verbose_name_plural = 'Department Budgets'
        ordering = ['-fiscal_year']


class DeanshipReport(models.Model):
    REPORT_TYPES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('special', 'Special Report'),
        ('performance', 'Performance Report'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dean = models.ForeignKey(Dean, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    report_period = models.CharField(max_length=50)
    content = models.TextField()
    statistics = models.JSONField(default=dict, blank=True)
    achievements = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    attachments = models.FileField(upload_to='deanship/reports/', null=True, blank=True)
    submitted_to = models.CharField(max_length=200, blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.dean.department.name} - {self.title} ({self.report_period})"
    
    class Meta:
        verbose_name = 'Deanship Report'
        verbose_name_plural = 'Deanship Reports'
        ordering = ['-created_at']
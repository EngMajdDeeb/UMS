from django.db import models
from django.contrib.auth.models import User
import uuid


class Faculty(models.Model):
    POSITION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('instructor', 'Instructor'),
        ('visiting_professor', 'Visiting Professor'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired'),
        ('on_leave', 'On Leave'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE)
    
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    
    # Professional Information
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)
    hire_date = models.DateField()
    office_location = models.CharField(max_length=100, blank=True)
    office_phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=200)
    education_qualifications = models.TextField()
    experience_years = models.IntegerField(default=0)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Academic Information
    research_interests = models.TextField(blank=True)
    publications = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.faculty_id} - {self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Faculty Member'
        verbose_name_plural = 'Faculty Members'
        ordering = ['faculty_id']


class FacultyQualification(models.Model):
    DEGREE_TYPES = [
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('postdoc', 'Post-Doctoral'),
        ('certificate', 'Certificate'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='qualifications')
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPES)
    degree_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    year_obtained = models.IntegerField()
    specialization = models.CharField(max_length=200, blank=True)
    grade = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.faculty.faculty_id} - {self.degree_name}"
    
    class Meta:
        verbose_name = 'Faculty Qualification'
        verbose_name_plural = 'Faculty Qualifications'


class FacultyLeave(models.Model):
    LEAVE_TYPES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('sabbatical', 'Sabbatical Leave'),
        ('emergency', 'Emergency Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.faculty.faculty_id} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    class Meta:
        verbose_name = 'Faculty Leave'
        verbose_name_plural = 'Faculty Leaves'
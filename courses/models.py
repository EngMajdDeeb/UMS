from django.db import models
from django.contrib.auth.models import User
import uuid


class Course(models.Model):
    COURSE_TYPES = [
        ('core', 'Core Course'),
        ('elective', 'Elective Course'),
        ('laboratory', 'Laboratory Course'),
        ('seminar', 'Seminar'),
        ('project', 'Project'),
        ('internship', 'Internship'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    credit_hours = models.IntegerField()
    contact_hours = models.IntegerField()
    description = models.TextField()
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    syllabus = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    assessment_methods = models.TextField(blank=True)
    textbooks = models.TextField(blank=True)
    reference_books = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['course_code']


class CourseOffering(models.Model):
    SEMESTER_CHOICES = [
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey('faculty.Faculty', on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    section = models.CharField(max_length=10)
    max_enrollment = models.IntegerField()
    current_enrollment = models.IntegerField(default=0)
    classroom = models.CharField(max_length=50, blank=True)
    schedule = models.TextField(blank=True)  # JSON format for time slots
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.course_code} - {self.semester} {self.year} Section {self.section}"
    
    class Meta:
        verbose_name = 'Course Offering'
        verbose_name_plural = 'Course Offerings'
        unique_together = ['course', 'semester', 'year', 'section']


class StudentEnrollment(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    final_grade = models.CharField(max_length=5, blank=True)
    grade_points = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.student_id} - {self.course_offering.course.course_code}"
    
    class Meta:
        verbose_name = 'Student Enrollment'
        verbose_name_plural = 'Student Enrollments'
        unique_together = ['student', 'course_offering']


class Assignment(models.Model):
    ASSIGNMENT_TYPES = [
        ('homework', 'Homework'),
        ('quiz', 'Quiz'),
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('project', 'Project'),
        ('presentation', 'Presentation'),
        ('lab', 'Lab Report'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    total_marks = models.IntegerField()
    weight_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    due_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course_offering.course.course_code} - {self.title}"
    
    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'


class StudentAssignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
        ('missing', 'Missing'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(null=True, blank=True)
    submission_file = models.FileField(upload_to='assignments/', null=True, blank=True)
    submission_text = models.TextField(blank=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    graded_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.student_id} - {self.assignment.title}"
    
    class Meta:
        verbose_name = 'Student Assignment'
        verbose_name_plural = 'Student Assignments'
        unique_together = ['student', 'assignment']
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
import uuid


class Client(TenantMixin):
    """
    Tenant model for universities
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # Settings for the tenant
    is_active = models.BooleanField(default=True)
    university_code = models.CharField(max_length=20, unique=True)
    university_type = models.CharField(max_length=50, choices=[
        ('public', 'Public University'),
        ('private', 'Private University'),
        ('technical', 'Technical University'),
        ('medical', 'Medical University'),
        ('arts', 'Arts University'),
    ], default='public')
    
    auto_create_schema = True
    auto_drop_schema = True
    
    class Meta:
        verbose_name = 'University Tenant'
        verbose_name_plural = 'University Tenants'
    
    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    Domain model for tenant routing
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        verbose_name = 'Tenant Domain'
        verbose_name_plural = 'Tenant Domains'
    
    def __str__(self):
        return self.domain
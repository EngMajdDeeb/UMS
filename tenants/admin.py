from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'university_code', 'university_type', 'is_active', 'created_on')
    list_filter = ('university_type', 'is_active', 'created_on')
    search_fields = ('name', 'university_code', 'description')
    readonly_fields = ('id', 'created_on', 'updated_on')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'university_code', 'university_type')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'updated_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('domain', 'tenant__name')
    readonly_fields = ('id',)
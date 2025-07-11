from rest_framework import serializers
from .models import Client, Domain


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'description', 'university_code', 'university_type', 
                 'is_active', 'created_on', 'updated_on']
        read_only_fields = ['id', 'created_on', 'updated_on']


class DomainSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = Domain
        fields = ['id', 'domain', 'tenant', 'tenant_name', 'is_primary']
        read_only_fields = ['id']
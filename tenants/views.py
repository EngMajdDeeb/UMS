from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Client, Domain
from .serializers import ClientSerializer, DomainSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def active_tenants(self, request):
        """Get all active tenants"""
        active_tenants = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_tenants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle tenant active status"""
        tenant = self.get_object()
        tenant.is_active = not tenant.is_active
        tenant.save()
        return Response({'status': 'success', 'is_active': tenant.is_active})


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_tenant(self, request):
        """Get domains for a specific tenant"""
        tenant_id = request.query_params.get('tenant_id')
        if tenant_id:
            domains = self.queryset.filter(tenant_id=tenant_id)
            serializer = self.get_serializer(domains, many=True)
            return Response(serializer.data)
        return Response({'error': 'tenant_id parameter required'}, status=400)
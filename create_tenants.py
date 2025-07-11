#!/usr/bin/env python3
import os
import sys
import django

# Add the project path to the Python path
sys.path.insert(0, '/app')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

from tenants.models import Client, Domain

# Create public tenant
public_tenant = Client(
    name='Public',
    schema_name='public',
    university_code='PUBLIC',
    university_type='public',
    description='Public tenant for shared data'
)
public_tenant.save()

# Create domain for public tenant
public_domain = Domain(
    tenant=public_tenant,
    domain='localhost',
    is_primary=True
)
public_domain.save()

print("✅ Public tenant created successfully!")
print(f"   Name: {public_tenant.name}")
print(f"   Schema: {public_tenant.schema_name}")
print(f"   Domain: {public_domain.domain}")

# Create sample university tenants
universities = [
    {'name': 'Yemen Public University', 'code': 'YPU', 'domain': 'ypu.localhost'},
    {'name': 'Amran Islamic University', 'code': 'AIU', 'domain': 'aiu.localhost'},
]

for uni in universities:
    tenant = Client(
        name=uni['name'],
        schema_name=uni['code'].lower(),
        university_code=uni['code'],
        university_type='public',
        description=f"{uni['name']} tenant"
    )
    tenant.save()
    
    domain = Domain(
        tenant=tenant,
        domain=uni['domain'],
        is_primary=True
    )
    domain.save()
    
    print(f"✅ Created tenant: {tenant.name}")
    print(f"   Schema: {tenant.schema_name}")
    print(f"   Domain: {domain.domain}")

print("\n🎉 All tenants created successfully!")
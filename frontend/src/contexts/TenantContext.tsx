import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface Tenant {
  id: string;
  name: string;
  university_code: string;
  university_type: string;
  description: string;
  is_active: boolean;
}

interface TenantContextType {
  tenants: Tenant[];
  currentTenant: Tenant | null;
  setCurrentTenant: (tenant: Tenant) => void;
  fetchTenants: () => Promise<void>;
  loading: boolean;
}

const TenantContext = createContext<TenantContextType | undefined>(undefined);

export const useTenant = () => {
  const context = useContext(TenantContext);
  if (!context) {
    throw new Error('useTenant must be used within a TenantProvider');
  }
  return context;
};

interface TenantProviderProps {
  children: ReactNode;
}

export const TenantProvider: React.FC<TenantProviderProps> = ({ children }) => {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [currentTenant, setCurrentTenant] = useState<Tenant | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchTenants = async () => {
    try {
      const response = await axios.get('/api/tenants/clients/');
      setTenants(response.data);
      
      // Set first active tenant as current if none selected
      if (!currentTenant && response.data.length > 0) {
        const activeTenant = response.data.find((t: Tenant) => t.is_active);
        if (activeTenant) {
          setCurrentTenant(activeTenant);
        }
      }
    } catch (error) {
      console.error('Failed to fetch tenants:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTenants();
  }, []);

  const value: TenantContextType = {
    tenants,
    currentTenant,
    setCurrentTenant,
    fetchTenants,
    loading
  };

  return (
    <TenantContext.Provider value={value}>
      {children}
    </TenantContext.Provider>
  );
};
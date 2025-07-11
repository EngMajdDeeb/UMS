import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { TenantProvider } from './contexts/TenantContext';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import StudentsPage from './pages/StudentsPage';
import FacultyPage from './pages/FacultyPage';
import CoursesPage from './pages/CoursesPage';
import DeanshipPage from './pages/DeanshipPage';
import TenantsPage from './pages/TenantsPage';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <TenantProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/" element={
                <ProtectedRoute>
                  <Layout>
                    <Dashboard />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/students" element={
                <ProtectedRoute>
                  <Layout>
                    <StudentsPage />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/faculty" element={
                <ProtectedRoute>
                  <Layout>
                    <FacultyPage />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/courses" element={
                <ProtectedRoute>
                  <Layout>
                    <CoursesPage />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/deanship" element={
                <ProtectedRoute>
                  <Layout>
                    <DeanshipPage />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/tenants" element={
                <ProtectedRoute>
                  <Layout>
                    <TenantsPage />
                  </Layout>
                </ProtectedRoute>
              } />
            </Routes>
          </div>
        </Router>
      </TenantProvider>
    </AuthProvider>
  );
}

export default App;
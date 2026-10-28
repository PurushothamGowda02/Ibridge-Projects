import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import DashboardLayout from './DashboardLayout';

const ProtectedRoute = ({ children, roles }: { children: React.ReactNode; roles?: string[] }) => {
  const { user, token, isLoading } = useAuth();

  if (isLoading) {
    return <div className="h-screen flex items-center justify-center text-primary font-bold">Loading LMS...</div>;
  }

  if (!token) {
    return <Navigate to="/login" />;
  }

  if (roles && !roles.includes(user?.role || '')) {
    return <Navigate to="/dashboard" />;
  }

  return <DashboardLayout>{children}</DashboardLayout>;
};

export default ProtectedRoute;

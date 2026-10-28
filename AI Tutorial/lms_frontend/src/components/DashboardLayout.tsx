import React from 'react';
import Sidebar from './Sidebar';

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex bg-bg-dark min-h-screen">
      <Sidebar />
      <main className="flex-1 px-10 py-8 overflow-y-auto h-screen bg-[radial-gradient(at_0%_0%,rgba(59,130,246,0.03)_0px,transparent_50%)]">
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;

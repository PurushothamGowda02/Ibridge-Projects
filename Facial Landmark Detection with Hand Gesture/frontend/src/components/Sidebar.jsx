import React from 'react';
import { Camera, Image, Info, ShieldCheck } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'detector', label: 'Real-time Detector', icon: Camera },
    { id: 'gallery', label: 'Snapshots Gallery', icon: Image },
  ];

  return (
    <aside className="glass" style={{ width: '280px', padding: '30px', display: 'flex', flexDirection: 'column', gap: '40px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ 
          background: 'linear-gradient(135deg, var(--primary), var(--secondary))', 
          width: '40px', 
          height: '40px', 
          borderRadius: '10px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <ShieldCheck size={24} color="white" />
        </div>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700 }}>VisionAI</h2>
      </div>

      <nav style={{ display: 'flex', flexDirection: 'column', gap: '10px', flex: 1 }}>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <div
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                background: isActive ? 'var(--glass)' : 'transparent',
                color: isActive ? 'var(--primary)' : 'var(--text-muted)',
                border: isActive ? '1px solid var(--border)' : '1px solid transparent'
              }}
            >
              <Icon size={20} />
              <span style={{ fontWeight: 600 }}>{item.label}</span>
            </div>
          );
        })}
      </nav>

      <div className="glass" style={{ padding: '20px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: 'var(--text)' }}>
          <Info size={16} />
          <span style={{ fontWeight: 600 }}>BCA Final Project</span>
        </div>
        <p>Facial Landmark & Gesture Detection System v1.0</p>
      </div>
    </aside>
  );
};

export default Sidebar;

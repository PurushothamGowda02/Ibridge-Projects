import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Detector from './components/Detector';
import Gallery from './components/Gallery';
import { LayoutDashboard, Image, Settings as SettingsIcon } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('detector');

  return (
    <div style={{ display: 'flex', width: '100%', height: '100vh', padding: '20px', gap: '20px' }}>
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>
        {activeTab === 'detector' && <Detector />}
        {activeTab === 'gallery' && <Gallery />}
      </main>
    </div>
  );
}

export default App;

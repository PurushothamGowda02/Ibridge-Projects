import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Trash2, Calendar, Fingerprint } from 'lucide-react';

const API_URL = "http://localhost:8000";

const Gallery = () => {
  const [snapshots, setSnapshots] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchSnapshots = async () => {
    try {
      const response = await axios.get(`${API_URL}/snapshots/`);
      setSnapshots(response.data);
    } catch (error) {
      console.error("Fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSnapshots();
  }, []);

  const deleteSnapshot = async (id) => {
    try {
      await axios.delete(`${API_URL}/snapshots/${id}`);
      setSnapshots(snapshots.filter(s => s.id !== id));
    } catch (error) {
      console.error("Delete error:", error);
    }
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '20px' }} className="animate-fade">
      <header className="glass" style={{ padding: '20px' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Snapshots Gallery</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Review detection history and captured gestures.</p>
      </header>

      {loading ? (
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <p>Loading gallery...</p>
        </div>
      ) : (
        <div style={{ 
          flex: 1, 
          overflowY: 'auto', 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
          gap: '20px',
          paddingBottom: '20px'
        }}>
          {snapshots.map((item) => (
            <div key={item.id} className="glass" style={{ overflow: 'hidden', position: 'relative' }}>
              <img 
                src={item.image_data} 
                alt="Snapshot" 
                style={{ width: '100%', height: '200px', objectFit: 'cover' }} 
              />
              <div style={{ padding: '15px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)', fontWeight: 600 }}>
                      <Fingerprint size={16} />
                      <span>{item.gesture_detected}</span>
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      Emotion: {item.emotion_detected}
                    </div>
                  </div>
                  <button 
                    onClick={() => deleteSnapshot(item.id)}
                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer' }}
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  <Calendar size={14} />
                  <span>{new Date(item.timestamp).toLocaleString()}</span>
                </div>
              </div>
            </div>
          ))}

          {snapshots.length === 0 && (
            <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '100px', color: 'var(--text-muted)' }}>
              <p>No snapshots yet. Use the Thumb Up gesture to capture one!</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Gallery;

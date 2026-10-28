import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Activity, LogOut, Bell } from 'lucide-react';
import axios from 'axios';

const Navbar = ({ user, setUser }) => {
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (user) {
      fetchUnreadCount();
      fetchNotifications();
      // Poll for new notifications every 30 seconds
      const interval = setInterval(() => {
        fetchUnreadCount();
        fetchNotifications();
      }, 30000);
      return () => clearInterval(interval);
    }
  }, [user]);

  const authHeaders = () => {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  const fetchUnreadCount = async () => {
    try {
      const res = await axios.get('http://localhost:8000/notifications/unread/count', { headers: authHeaders() });
      setUnreadCount(res.data.count);
    } catch (err) {
      console.error('Error fetching unread count', err);
    }
  };

  const fetchNotifications = async () => {
    try {
      const res = await axios.get('http://localhost:8000/notifications', { headers: authHeaders() });
      setNotifications(res.data);
    } catch (err) {
      console.error('Error fetching notifications', err);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      await axios.put(`http://localhost:8000/notifications/${notificationId}/read`, {}, { headers: authHeaders() });
      fetchUnreadCount();
      fetchNotifications();
    } catch (err) {
      console.error('Error marking notification as read', err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate('/');
  };

  return (
    <nav className="nav-shell glass container">
      <div className="nav-content">
        <Link to="/" className="nav-brand">
          <Activity size={25} />
          <span>Web Doctor</span>
        </Link>

        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/hospitals" className="nav-link">Hospitals</Link>
          {user && <Link to="/dashboard" className="nav-link">Dashboard</Link>}

          {user ? (
            <>
              {/* Notification Bell */}
              <div style={{ position: 'relative' }}>
                <button 
                  onClick={() => setShowNotifications(!showNotifications)}
                  style={{ 
                    background: 'transparent', 
                    border: 'none', 
                    cursor: 'pointer',
                    position: 'relative',
                    padding: '0.5rem'
                  }}
                  aria-label="Notifications"
                >
                  <Bell size={20} color="var(--text)" />
                  {unreadCount > 0 && (
                    <span style={{
                      position: 'absolute',
                      top: '0',
                      right: '0',
                      background: 'var(--danger)',
                      color: 'white',
                      borderRadius: '50%',
                      width: '18px',
                      height: '18px',
                      fontSize: '0.7rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 'bold'
                    }}>
                      {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                  )}
                </button>

                {/* Notifications Dropdown */}
                {showNotifications && (
                  <div style={{
                    position: 'absolute',
                    top: '100%',
                    right: '0',
                    marginTop: '0.5rem',
                    width: '350px',
                    maxHeight: '400px',
                    overflowY: 'auto',
                    background: 'white',
                    border: '1px solid var(--border)',
                    borderRadius: '0.5rem',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                    zIndex: 1000
                  }}>
                    <div style={{ 
                      padding: '1rem', 
                      borderBottom: '1px solid var(--border)',
                      fontWeight: 'bold'
                    }}>
                      Notifications
                    </div>
                    {notifications.length === 0 ? (
                      <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                        No notifications
                      </div>
                    ) : (
                      notifications.slice(0, 10).map((notif) => (
                        <div 
                          key={notif.id}
                          onClick={() => markAsRead(notif.id)}
                          style={{
                            padding: '1rem',
                            borderBottom: '1px solid var(--border)',
                            cursor: 'pointer',
                            background: notif.is_read === 0 ? 'rgba(99, 102, 241, 0.05)' : 'white',
                            transition: 'background 0.2s'
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.background = 'var(--surface-muted)'}
                          onMouseLeave={(e) => e.currentTarget.style.background = notif.is_read === 0 ? 'rgba(99, 102, 241, 0.05)' : 'white'}
                        >
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                            <p style={{ fontWeight: 600, margin: '0 0 0.25rem 0', fontSize: '0.9rem' }}>
                              {notif.title}
                            </p>
                            {notif.is_read === 0 && (
                              <span style={{
                                width: '8px',
                                height: '8px',
                                background: 'var(--brand)',
                                borderRadius: '50%',
                                display: 'inline-block'
                              }} />
                            )}
                          </div>
                          <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                            {notif.message}
                          </p>
                          <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                            {new Date(notif.created_at).toLocaleString('en-IN', {
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>

              <span style={{ color: 'var(--text-muted)', fontWeight: 700 }}>{user.full_name}</span>
              <button onClick={handleLogout} className="btn btn-outline" aria-label="Logout">
                <LogOut size={16} /> Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-outline">Login</Link>
              <Link to="/register" className="btn btn-primary">Create Account</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

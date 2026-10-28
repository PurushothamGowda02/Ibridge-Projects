import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, User, LogOut, LayoutDashboard } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav className="glass-morphism" style={{ 
            margin: '20px', 
            position: 'sticky', 
            top: '20px', 
            zIndex: 1000, 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            padding: '12px 30px' 
        }}>
            <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '1.5rem', fontWeight: 'bold' }}>
                <Heart className="text-secondary" fill="#ec4899" size={32} />
                <span>PetRescue</span>
            </Link>

            <div style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
                <Link to="/">Home</Link>
                <Link to="/adopt">Adopt</Link>
                <Link to="/report">Report Stray</Link>
                <Link to="/donate">Donate</Link>
                
                {user ? (
                    <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                        {user.role === 'admin' && (
                            <Link to="/admin" style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--primary-color)' }}>
                                <LayoutDashboard size={18} />
                                Dashboard
                            </Link>
                        )}
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{ color: 'var(--muted-text)', fontSize: '0.9rem' }}>
                                Hi, {user.username}
                            </span>
                            <button onClick={handleLogout} className="btn glass-morphism" style={{ padding: '8px 16px', fontSize: '0.9rem' }}>
                                <LogOut size={16} />
                                Logout
                            </button>
                        </div>
                    </div>
                ) : (
                    <Link to="/login" className="btn btn-primary">
                        <User size={18} />
                        Login
                    </Link>
                )}
            </div>
        </nav>
    );
};

export default Navbar;

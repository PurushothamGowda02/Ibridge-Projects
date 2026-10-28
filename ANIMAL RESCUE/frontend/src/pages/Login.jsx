import React, { useState } from 'react';
import { Mail, Lock, LogIn, UserPlus, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login, register } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                await login(username || email.split('@')[0], password); // Simple fallback for demo
            } else {
                await register(username, email, password);
            }
            navigate('/'); // Redirect to home on success
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-morphism" 
                style={{ padding: '50px', width: '100%', maxWidth: '450px' }}
            >
                <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                    <h1 style={{ fontSize: '2.5rem', marginBottom: '8px' }}>
                        {isLogin ? 'Welcome Back' : 'Join Us'}
                    </h1>
                    <p style={{ color: 'var(--muted-text)' }}>
                        {isLogin ? 'Login to manage your adoptions' : 'Create an account to start adopting'}
                    </p>
                </div>

                {error && (
                    <div style={{ 
                        background: 'rgba(239, 68, 68, 0.1)', 
                        border: '1px solid #ef4444', 
                        color: '#ef4444', 
                        padding: '12px', 
                        borderRadius: '12px', 
                        marginBottom: '24px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px'
                    }}>
                        <AlertCircle size={18} />
                        <span style={{ fontSize: '0.9rem' }}>{error}</span>
                    </div>
                )}

                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    {!isLogin && (
                        <div style={{ position: 'relative' }}>
                            <Mail style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted-text)' }} size={20} />
                            <input 
                                required
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                style={{ 
                                    width: '100%', 
                                    background: 'rgba(255,255,255,0.05)', 
                                    border: '1px solid var(--glass-border)', 
                                    borderRadius: '12px', 
                                    padding: '16px 16px 16px 50px', 
                                    color: 'white',
                                    outline: 'none'
                                }}
                            />
                        </div>
                    )}
                    <div style={{ position: 'relative' }}>
                        <Mail style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted-text)' }} size={20} />
                        <input 
                            required
                            type="text"
                            placeholder={isLogin ? "Username or Email" : "Email Address"}
                            value={isLogin && !username ? email : (isLogin ? username : email)}
                            onChange={(e) => isLogin ? setUsername(e.target.value) : setEmail(e.target.value)}
                            style={{ 
                                width: '100%', 
                                background: 'rgba(255,255,255,0.05)', 
                                border: '1px solid var(--glass-border)', 
                                borderRadius: '12px', 
                                padding: '16px 16px 16px 50px', 
                                color: 'white',
                                outline: 'none'
                            }}
                        />
                    </div>
                    <div style={{ position: 'relative' }}>
                        <Lock style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted-text)' }} size={20} />
                        <input 
                            required
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{ 
                                width: '100%', 
                                background: 'rgba(255,255,255,0.05)', 
                                border: '1px solid var(--glass-border)', 
                                borderRadius: '12px', 
                                padding: '16px 16px 16px 50px', 
                                color: 'white',
                                outline: 'none'
                            }}
                        />
                    </div>

                    <button 
                        type="submit" 
                        className="btn btn-primary" 
                        style={{ padding: '16px', justifyContent: 'center' }}
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : (isLogin ? <><LogIn size={20} /> Login</> : <><UserPlus size={20} /> Register</>)}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '32px' }}>
                    <p style={{ color: 'var(--muted-text)' }}>
                        {isLogin ? "Don't have an account?" : "Already have an account?"}
                        <button 
                            type="button"
                            onClick={() => setIsLogin(!isLogin)}
                            style={{ 
                                background: 'none', 
                                border: 'none', 
                                color: 'var(--primary-color)', 
                                fontWeight: 'bold', 
                                marginLeft: '8px', 
                                cursor: 'pointer' 
                            }}
                        >
                            {isLogin ? 'Sign Up' : 'Login'}
                        </button>
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default Login;

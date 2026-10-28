import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { User, Mail, Lock, Stethoscope, AlertTriangle, Phone } from 'lucide-react';

const Auth = ({ setUser, isLogin = true }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [role, setRole] = useState('patient');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const tokenRes = await axios.post('http://localhost:8000/token', formData);
        localStorage.setItem('token', tokenRes.data.access_token);

        const userRes = await axios.get('http://localhost:8000/me', {
          headers: { Authorization: `Bearer ${tokenRes.data.access_token}` },
        });
        setUser(userRes.data);
        navigate('/dashboard');
        return;
      }

      await axios.post('http://localhost:8000/register', {
        email,
        password,
        full_name: fullName,
        phone_number: phoneNumber,
        role,
      });

      alert('Account created successfully! Please login with your credentials.');
      navigate('/login');
    } catch (err) {
      console.error('Auth error:', err);
      let errorMessage = 'Authentication failed. Please verify your details.';
      
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message === 'Network Error') {
        errorMessage = 'Cannot connect to server. Please ensure the backend is running on http://localhost:8000';
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      if (isLogin) {
        errorMessage = 'Login failed: ' + errorMessage;
      } else {
        errorMessage = 'Registration failed: ' + errorMessage;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="section">
      <div className="container" style={{ display: 'grid', placeItems: 'center' }}>
        <div className="card" style={{ width: 'min(470px, 100%)' }}>
          <h1 style={{ fontSize: '2rem' }}>{isLogin ? 'Sign in to Web Doctor' : 'Create your medical account'}</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: '0.35rem' }}>
            {isLogin ? 'Access your triage dashboard and appointments.' : 'Start with free symptom triage and low-cost care guidance.'}
          </p>

          {error && (
            <div className="warning-panel" style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
              <AlertTriangle size={16} color="var(--danger)" />
              <p style={{ color: 'var(--danger)', fontWeight: 700 }}>{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ marginTop: '1.2rem' }}>
            {!isLogin && (
              <>
                <div className="input-group">
                  <label>Full Name</label>
                  <div style={{ position: 'relative' }}>
                    <User size={16} style={{ position: 'absolute', left: '0.75rem', top: '0.86rem', color: 'var(--text-muted)' }} />
                    <input
                      required
                      type="text"
                      value={fullName}
                      placeholder="Enter your name"
                      style={{ paddingLeft: '2.2rem' }}
                      onChange={(e) => setFullName(e.target.value)}
                    />
                  </div>
                </div>

                <div className="input-group">
                  <label>Phone Number</label>
                  <div style={{ position: 'relative' }}>
                    <Phone size={16} style={{ position: 'absolute', left: '0.75rem', top: '0.86rem', color: 'var(--text-muted)' }} />
                    <input
                      required
                      type="tel"
                      value={phoneNumber}
                      placeholder="Enter your phone number"
                      style={{ paddingLeft: '2.2rem' }}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                  </div>
                </div>

                <div className="input-group">
                  <label>Join As</label>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.55rem' }}>
                    <button type="button" className={`btn ${role === 'patient' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setRole('patient')}>
                      <User size={16} /> Patient
                    </button>
                    <button type="button" className={`btn ${role === 'doctor' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setRole('doctor')}>
                      <Stethoscope size={16} /> Doctor
                    </button>
                  </div>
                </div>
              </>
            )}

            <div className="input-group">
              <label>Email</label>
              <div style={{ position: 'relative' }}>
                <Mail size={16} style={{ position: 'absolute', left: '0.75rem', top: '0.86rem', color: 'var(--text-muted)' }} />
                <input
                  required
                  type="email"
                  value={email}
                  placeholder="you@example.com"
                  style={{ paddingLeft: '2.2rem' }}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <div className="input-group">
              <label>Password</label>
              <div style={{ position: 'relative' }}>
                <Lock size={16} style={{ position: 'absolute', left: '0.75rem', top: '0.86rem', color: 'var(--text-muted)' }} />
                <input
                  required
                  type="password"
                  value={password}
                  placeholder="Enter password"
                  style={{ paddingLeft: '2.2rem' }}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '0.35rem' }} disabled={loading}>
              {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
            </button>
          </form>

          <p style={{ marginTop: '0.95rem', color: 'var(--text-muted)' }}>
            {isLogin ? "Do not have an account?" : 'Already registered?'}{' '}
            <button
              type="button"
              onClick={() => navigate(isLogin ? '/register' : '/login')}
              style={{ border: 'none', background: 'transparent', color: 'var(--brand)', fontWeight: 800, cursor: 'pointer' }}
            >
              {isLogin ? 'Create one' : 'Sign in'}
            </button>
          </p>
        </div>
      </div>
    </section>
  );
};

export default Auth;

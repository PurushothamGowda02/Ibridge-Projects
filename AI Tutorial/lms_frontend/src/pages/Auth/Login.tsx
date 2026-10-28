import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, Loader, ArrowRight, BookOpen, AlertCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { authApi } from '../../services/authApi';
import { AxiosError } from 'axios';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await authApi.login({ email, password });
      
      // Check if user is a student
      const userRole = response.data.user?.role || response.data.role || 'student';
      
      if (userRole !== 'student') {
        setError('Only students can login through this portal. Please contact your administrator.');
        setIsLoading(false);
        return;
      }

      const userPayload = {
        email,
        name: response.data.user?.name || email.split('@')[0],
        role: userRole,
        eligibility_test_passed: response.data.user?.eligibility_test_passed || false,
        eligibility_test_score: response.data.user?.eligibility_test_score || 0,
      };
      
      login(response.data.token, userPayload);
      
      // Check if eligibility test is passed
      if (!userPayload.eligibility_test_passed) {
        // Redirect to eligibility test
        navigate('/pre-eligibility');
      } else {
        // Redirect to dashboard
        navigate('/dashboard');
      }
    } catch (err: unknown) {
      const message = err instanceof AxiosError ? (err.response?.data as { message?: string } | undefined)?.message : undefined;
      setError(message || 'Login failed. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(at_0%_0%,rgba(59,130,246,0.05)_0px,transparent_50%),radial-gradient(at_100%_100%,rgba(168,85,247,0.05)_0px,transparent_50%)]">
      {/* Header */}
      <div className="border-b border-white/10 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="text-primary" size={28} />
            <span className="text-xl font-bold">AI Tutorial LMS</span>
          </div>
          <p className="text-white/60 text-sm">New here? <Link to="/signup" className="text-primary hover:underline font-semibold">Create Account</Link></p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12 flex items-center justify-center min-h-[calc(100vh-80px)]">
        <div className="max-w-md w-full">
          <div className="text-center mb-10">
            <h1 className="text-4xl font-extrabold tracking-tight mb-2">
              Welcome <span className="text-primary">Back</span>
            </h1>
            <p className="text-white/60">Sign in to your student account to continue learning.</p>
          </div>

          <div className="glass-card">
            <form onSubmit={handleLogin} className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-white/70 ml-1">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40" size={18} />
                  <input
                    type="email"
                    required
                    placeholder="name@example.com"
                    className="input-field w-full pl-12"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-white/70 ml-1">Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40" size={18} />
                  <input
                    type="password"
                    required
                    placeholder="••••••••"
                    className="input-field w-full pl-12"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
              </div>

              {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-500 text-sm p-3 rounded-xl flex gap-2 items-start">
                  <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              <button type="submit" className="btn-primary w-full flex items-center justify-center gap-2 group" disabled={isLoading}>
                {isLoading ? <Loader className="animate-spin" size={20} /> : (
                  <>
                    Sign In <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>

            <div className="mt-8 pt-6 border-t border-white/10">
              <p className="text-center text-white/50 text-sm">
                Don't have an account?{' '}
                <Link to="/signup" className="text-primary hover:underline font-semibold">
                  Register here
                </Link>
              </p>
            </div>
          </div>

          <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <p className="text-sm text-blue-400">
              <span className="font-semibold">Student Portal:</span> This login is exclusively for registered students. Instructors and administrators should use their respective portals.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

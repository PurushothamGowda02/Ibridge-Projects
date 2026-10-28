// import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, BookOpen, MessageSquare, Award, 
  LogOut, PlusCircle, Sparkles, ClipboardCheck, MessageCircle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
    { icon: BookOpen, label: 'Course Library', path: '/library' },
    { icon: Award, label: 'My Learning', path: '/my-courses' },
    { icon: ClipboardCheck, label: 'Pre-Eligibility', path: '/pre-eligibility' },
    { icon: Sparkles, label: 'AI Tutor Lab', path: '/ai-tutor' },
    { icon: MessageCircle, label: 'AI Chatbot', path: '/chatbot' },
    { icon: MessageSquare, label: 'Discussions', path: '/discussions' },
  ];

  if (user?.role === 'instructor' || user?.role === 'admin') {
    menuItems.push(
      { icon: PlusCircle, label: 'Course Builder', path: '/instructor/builder' },
      { icon: Sparkles, label: 'AI Architect', path: '/instructor/ai-creator' }
    );
  }

  return (
    <aside className="w-72 bg-bg-secondary border-r border-white/5 flex flex-col h-screen sticky top-0">
      <div className="p-8">
        <h1 className="text-2xl font-black tracking-tighter text-white">
          ANTIGRAVITY<span className="text-primary italic">LMS</span>
        </h1>
      </div>

      <nav className="flex-1 px-4 space-y-2">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                isActive 
                ? 'bg-primary/10 text-primary border border-primary/20 shadow-[0_0_20px_rgba(59,130,246,0.1)]' 
                : 'text-white/50 hover:bg-white/5 hover:text-white'
              }`
            }
          >
            <item.icon size={20} />
            <span className="font-semibold">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-6 mt-auto border-t border-white/5">
        <div className="bg-bg-accent/50 rounded-2xl p-4 mb-4">
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center font-bold text-white shadow-lg">
              {user?.name?.[0].toUpperCase()}
            </div>
            <div className="overflow-hidden">
              <p className="text-sm font-bold text-white truncate">{user?.name}</p>
              <p className="text-xs text-white/40 capitalize">{user?.role}</p>
            </div>
          </div>
        </div>
        
        <button 
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-red-400 hover:bg-red-500/10 transition-colors duration-200 group"
        >
          <LogOut size={20} />
          <span className="font-semibold">Sign Out</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;

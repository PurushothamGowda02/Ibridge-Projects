import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { lmsApi } from '../../services/lmsApi';
import type { PerformanceResponse, WeakTopicItem, PerformanceHistoryItem } from '../../services/apiTypes';
import { useToast } from '../../components/ToastProvider';
import { getErrorMessage } from '../../utils/errors';

const DashboardHome = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();
  const [isLoading, setIsLoading] = useState(true);
  const [streak, setStreak] = useState(0);
  const [performance, setPerformance] = useState<PerformanceResponse | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [streakRes, perfRes] = await Promise.all([
          lmsApi.getStreak(),
          lmsApi.getPerformance(),
        ]);
        setStreak(streakRes.data?.streak || 0);
        setPerformance(perfRes.data || null);
      } catch (error) {
        console.error('Dashboard metrics fetch failed', error);
        toast.error(getErrorMessage(error, 'Failed to load dashboard metrics.'));
      } finally {
        setIsLoading(false);
      }
    };
    load();
  }, [toast]);

  const weakTopics = performance?.weak_topics || [];
  const history = performance?.history || [];
  const mastery = performance?.mastery || [];

  if (isLoading) {
    return <div className="h-40 flex items-center justify-center text-white/50">Loading dashboard metrics...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex justify-between items-end mb-10">
        <div>
          <p className="text-white/40 font-bold uppercase tracking-widest text-xs mb-2">Welcome Back</p>
          <h2 className="text-4xl font-extrabold tracking-tight">Ready to <span className="text-primary italic">Learn</span>, {user?.name.split(' ')[0]}?</h2>
        </div>
        <div className="glass-card py-3 px-6 border-l-4 border-l-orange-500">
          <p className="text-xs text-white/40 font-bold uppercase">Current Streak</p>
          <p className="text-2xl font-black italic">{streak} DAYS</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-8">
        <div className="glass-card p-6">
          <p className="text-xs text-white/40 font-bold uppercase">Recent Attempts</p>
          <p className="text-3xl font-black mt-2">{history.length}</p>
          <button onClick={() => navigate('/my-courses')} className="mt-6 text-xs font-black text-primary uppercase tracking-widest hover:underline">View Progress</button>
        </div>
        <div className="glass-card p-6">
          <p className="text-xs text-white/40 font-bold uppercase">Mastery Topics</p>
          <p className="text-3xl font-black mt-2">{mastery.length}</p>
          <button onClick={() => navigate('/my-courses')} className="mt-6 text-xs font-black text-primary uppercase tracking-widest hover:underline">Open Analytics</button>
        </div>
        <div className="glass-card p-6">
          <p className="text-xs text-white/40 font-bold uppercase">Weak Topics</p>
          <p className="text-3xl font-black mt-2">{weakTopics.length}</p>
          <button onClick={() => navigate('/ai-tutor')} className="mt-6 text-xs font-black text-primary uppercase tracking-widest hover:underline">Start Practice</button>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="glass-card p-6">
          <p className="text-xs text-white/40 font-bold uppercase mb-4">Focus Next</p>
          {weakTopics.length === 0 ? (
            <p className="text-white/50 text-sm">No weak topics yet. Complete tests in AI Tutor to personalize this list.</p>
          ) : (
            <div className="space-y-3">
              {weakTopics.slice(0, 4).map((w: WeakTopicItem, idx: number) => (
                <button
                  key={idx}
                  onClick={() => navigate(`/ai-tutor?subject=Programming&topic=${encodeURIComponent(w._id || 'General')}`)}
                  className="w-full text-left p-3 rounded-xl bg-white/5 hover:bg-white/10"
                >
                  <p className="font-bold">{w._id || 'General'}</p>
                  <p className="text-xs text-white/50 mt-1">Avg: {Math.round(w.avg_score || 0)}% | Attempts: {w.attempts || 0}</p>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="glass-card p-6">
          <p className="text-xs text-white/40 font-bold uppercase mb-4">Latest Results</p>
          {history.length === 0 ? (
            <p className="text-white/50 text-sm">No attempts recorded yet.</p>
          ) : (
            <div className="space-y-3">
              {history.slice(0, 4).map((h: PerformanceHistoryItem, idx: number) => (
                <div key={idx} className="p-3 rounded-xl bg-white/5">
                  <p className="font-semibold">{h.topic}</p>
                  <p className="text-xs text-white/50 mt-1">{h.date} - Score: {Math.round(h.score || 0)}%</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;

import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart3, Flame, Target, TrendingDown, Sparkles } from 'lucide-react';
import { lmsApi, STORAGE_KEYS } from '../../services/lmsApi';
import type { PerformanceResponse, WeakTopicItem, PerformanceHistoryItem } from '../../services/apiTypes';
import { useToast } from '../../components/ToastProvider';
import { getErrorMessage } from '../../utils/errors';

const MyCourses = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [isLoading, setIsLoading] = useState(true);
  const [streak, setStreak] = useState(0);
  const [performance, setPerformance] = useState<PerformanceResponse | null>(null);
  const [savedCourses, setSavedCourses] = useState<Array<{ id: string; title: string; joined: boolean; progress_percent: number; pretest_percent: number; course: unknown }>>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const [streakRes, perfRes] = await Promise.all([
          lmsApi.getStreak(),
          lmsApi.getPerformance(),
        ]);
        setStreak(streakRes.data?.streak || 0);
        setPerformance(perfRes.data || null);
        const coursesRes = await lmsApi.myCourses();
        setSavedCourses(coursesRes.data || []);
      } catch (err) {
        console.error('Failed to load learning analytics', err);
        toast.error(getErrorMessage(err, 'Failed to load learning analytics.'));
      } finally {
        setIsLoading(false);
      }
    };
    load();
  }, [toast]);

  if (isLoading) return <div className="h-40 flex items-center justify-center">Loading your learning analytics...</div>;

  const weakTopics = performance?.weak_topics || [];
  const mastery = performance?.mastery || [];
  const history = performance?.history || [];

  return (
    <div className="max-w-7xl mx-auto pb-20 space-y-8">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-4xl font-extrabold tracking-tight">My <span className="text-primary italic">Learning</span></h2>
          <p className="text-white/40 font-medium">Track progress, weak areas, and continue your AI-driven study plan.</p>
        </div>
        <button onClick={() => navigate('/ai-tutor')} className="btn-primary flex items-center gap-2">
          <Sparkles size={16} /> Continue AI Tutor
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card">
          <div className="flex items-center gap-2 text-white/60 text-sm mb-2"><Flame size={16} /> Streak</div>
          <p className="text-3xl font-black">{streak} days</p>
        </div>
        <div className="glass-card">
          <div className="flex items-center gap-2 text-white/60 text-sm mb-2"><BarChart3 size={16} /> Attempts</div>
          <p className="text-3xl font-black">{history.length}</p>
        </div>
        <div className="glass-card">
          <div className="flex items-center gap-2 text-white/60 text-sm mb-2"><Target size={16} /> Mastery Topics</div>
          <p className="text-3xl font-black">{mastery.length}</p>
        </div>
      </div>

      <section className="glass-card space-y-4">
        <h3 className="font-black text-xl">Saved Courses</h3>
        {savedCourses.length === 0 ? (
          <p className="text-white/40 text-sm">No saved courses yet. Generate and save one from AI Tutor.</p>
        ) : (
          <div className="space-y-3">
            {savedCourses.map((c) => (
              <div key={c.id} className="p-4 rounded-xl bg-white/5 flex items-center justify-between gap-4">
                <div>
                  <p className="font-bold">{c.title}</p>
                  <p className="text-xs text-white/50 mt-1">
                    {c.joined ? 'Joined' : 'Saved only'} | Progress: {c.progress_percent}% | Pre-test: {c.pretest_percent}%
                  </p>
                </div>
                <button
                  className="btn-primary"
                  onClick={() => {
                    localStorage.setItem(STORAGE_KEYS.aiGeneratedCourse, JSON.stringify(c.course));
                    navigate('/learn-ai');
                  }}
                >
                  Continue
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section className="glass-card space-y-4">
          <div className="flex items-center gap-2"><TrendingDown size={18} /><h3 className="font-black">Weak Topics (Focus Next)</h3></div>
          {weakTopics.length === 0 ? (
            <p className="text-white/40 text-sm">No weak topics yet. Start quizzes/coding in AI Tutor to build your profile.</p>
          ) : (
            <div className="space-y-3">
              {weakTopics.map((w: WeakTopicItem, idx: number) => (
                <button
                  key={idx}
                  onClick={() => navigate(`/ai-tutor?subject=Programming&topic=${encodeURIComponent(w._id || 'General')}`)}
                  className="w-full text-left p-4 rounded-xl bg-white/5 hover:bg-white/10 transition"
                >
                  <p className="font-bold">{w._id || 'General'}</p>
                  <p className="text-xs text-white/50 mt-1">Avg score: {Math.round(w.avg_score || 0)}% | Attempts: {w.attempts || 0}</p>
                </button>
              ))}
            </div>
          )}
        </section>

        <section className="glass-card space-y-4">
          <div className="flex items-center gap-2"><BarChart3 size={18} /><h3 className="font-black">Recent Performance</h3></div>
          {history.length === 0 ? (
            <p className="text-white/40 text-sm">No attempts recorded yet.</p>
          ) : (
            <div className="space-y-3">
              {history.map((h: PerformanceHistoryItem, idx: number) => (
                <div key={idx} className="p-4 rounded-xl bg-white/5">
                  <p className="font-bold">{h.topic}</p>
                  <p className="text-xs text-white/50 mt-1">{h.date} - Score: {Math.round(h.score || 0)}%</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default MyCourses;

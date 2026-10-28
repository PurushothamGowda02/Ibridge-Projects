import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Sparkles, PlayCircle, Code2, BarChart3 } from 'lucide-react';
import { lmsApi, STORAGE_KEYS } from '../../services/lmsApi';
import { useToast } from '../../components/ToastProvider';
import { getErrorMessage } from '../../utils/errors';
import type {
  CodingPracticeResponse,
  CodingSubmissionResponse,
  GeneratedCourseResponse,
  GeneratedTestResponse,
  LmsVideosResponse,
  PerformanceResponse,
  PerformanceHistoryItem,
  WeakTopicItem,
  VideoItem,
} from '../../services/apiTypes';

const AiTutorLab = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [searchParams] = useSearchParams();
  const [subject, setSubject] = useState(() => searchParams.get('subject') || 'Programming');
  const [topic, setTopic] = useState(() => searchParams.get('topic') || 'Python OOP');
  const [difficulty, setDifficulty] = useState('Intermediate');

  const [videos, setVideos] = useState<LmsVideosResponse | null>(null);
  const [course, setCourse] = useState<GeneratedCourseResponse | null>(null);
  const [testData, setTestData] = useState<GeneratedTestResponse | null>(null);
  const [codingData, setCodingData] = useState<CodingPracticeResponse | null>(null);
  const [performance, setPerformance] = useState<PerformanceResponse | null>(null);
  const [codingSubmission, setCodingSubmission] = useState('def solve():\n    pass');
  const [codingFeedback, setCodingFeedback] = useState<CodingSubmissionResponse | null>(null);
  const [isLoading, setIsLoading] = useState<string | null>(null);
  const [activeVideoUrl, setActiveVideoUrl] = useState<string | null>(null);

  const getYouTubeId = (url?: string) => {
    if (!url) return null;
    const match = url.match(/(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{11})/);
    return match?.[1] || null;
  };

  const runAction = async (action: string, fn: () => Promise<void>) => {
    try {
      setIsLoading(action);
      await fn();
    } catch (error) {
      console.error(action, error);
      toast.error(`${action} failed: ${getErrorMessage(error)}`);
    } finally {
      setIsLoading(null);
    }
  };

  const fetchVideos = () => runAction('videos', async () => {
    const res = await lmsApi.getVideos({ subject, topic, personalize: true });
    setVideos(res.data);
  });

  const generateCourse = () => runAction('course', async () => {
    const res = await lmsApi.generateCourse({ topic });
    setCourse(res.data);
    localStorage.setItem(STORAGE_KEYS.aiGeneratedCourse, JSON.stringify(res.data));
    toast.success('AI course generated successfully.');
  });

  const generateTest = () => runAction('test', async () => {
    const res = await lmsApi.generateTest({ topic, difficulty, type: 'mixed' });
    setTestData(res.data);
  });

  const generateCoding = () => runAction('coding', async () => {
    const res = await lmsApi.generateCodingPractice({ subject, topic, difficulty });
    setCodingData(res.data);
  });

  const submitCoding = () => runAction('submit-coding', async () => {
    const problem = codingData?.problems?.[0];
    const res = await lmsApi.submitCoding({
      subject,
      topic,
      problem_id: problem?.id || 'p1',
      language: 'python',
      code: codingSubmission,
      problem_statement: problem?.description || topic,
    });
    setCodingFeedback(res.data);
    toast.info('Coding submission evaluated.');
  });

  const loadPerformance = () => runAction('performance', async () => {
    const res = await lmsApi.getPerformance();
    setPerformance(res.data);
  });

  return (
    <div className="max-w-7xl mx-auto pb-20 space-y-8">
      <div>
        <h2 className="text-4xl font-black tracking-tight mb-2">AI Tutor <span className="text-primary italic">Lab</span></h2>
        <p className="text-white/40">Personalized videos, AI tests, coding practice, and performance insights.</p>
      </div>

      <div className="glass-card grid grid-cols-1 md:grid-cols-4 gap-4">
        <input className="input-field" value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Subject" />
        <input className="input-field" value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Topic" />
        <select className="input-field" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>
        </select>
        <button className="btn-primary" onClick={fetchVideos} disabled={isLoading === 'videos'}>
          {isLoading === 'videos' ? 'Loading...' : 'Fetch Videos'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section className="glass-card space-y-4">
          <div className="flex items-center gap-2"><PlayCircle size={18} /><h3 className="font-black">Clustered Videos</h3></div>
          {videos?.video_clusters ? Object.entries(videos.video_clusters).map(([cluster, items]) => (
            <div key={cluster}>
              <p className="text-sm font-bold text-primary mb-2">{cluster}</p>
              <div className="space-y-2">
                {(items as VideoItem[]).map((v) => (
                  <button
                    key={v.id}
                    type="button"
                    onClick={() => setActiveVideoUrl(v.link)}
                    className="block text-left w-full text-sm text-white/80 hover:text-primary truncate"
                  >
                    {v.title}
                  </button>
                ))}
              </div>
            </div>
          )) : <p className="text-white/40 text-sm">No videos loaded.</p>}
          {activeVideoUrl && getYouTubeId(activeVideoUrl) ? (
            <div className="mt-4">
              <iframe
                className="w-full aspect-video rounded-xl"
                src={`https://www.youtube.com/embed/${getYouTubeId(activeVideoUrl)}?autoplay=1&rel=0`}
                title="Video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          ) : null}
        </section>

        <section className="glass-card space-y-4">
          <div className="flex items-center gap-2"><Sparkles size={18} /><h3 className="font-black">AI Course + Test</h3></div>
          <div className="flex gap-3">
            <button className="btn-primary" onClick={generateCourse} disabled={isLoading === 'course'}>Generate Course</button>
            <button className="btn-primary bg-white/10 hover:bg-white/20" onClick={generateTest} disabled={isLoading === 'test'}>Generate Test</button>
            <button className="btn-primary bg-white/10 hover:bg-white/20" onClick={() => navigate('/learn-ai')} disabled={!course}>Open Course Player</button>
          </div>
          {course?.modules?.length ? <p className="text-sm text-white/70">Modules: {course.modules.length}</p> : null}
          {testData?.questions?.length ? <p className="text-sm text-white/70">Test Questions: {testData.questions.length}</p> : null}
        </section>

        <section className="glass-card space-y-4 lg:col-span-2">
          <div className="flex items-center gap-2"><Code2 size={18} /><h3 className="font-black">Coding Practice + AI Evaluation</h3></div>
          <div className="flex gap-3 flex-wrap">
            <button className="btn-primary" onClick={generateCoding} disabled={isLoading === 'coding'}>Generate Coding Problems</button>
            <button className="btn-primary bg-white/10 hover:bg-white/20" onClick={submitCoding} disabled={isLoading === 'submit-coding'}>Submit Code</button>
          </div>
          {codingData?.problems?.[0] ? (
            <div className="bg-white/5 rounded-xl p-4">
              <p className="font-bold">{codingData.problems[0].title}</p>
              <p className="text-sm text-white/70 mt-1">{codingData.problems[0].description}</p>
            </div>
          ) : null}
          <textarea
            className="input-field w-full min-h-40"
            value={codingSubmission}
            onChange={(e) => setCodingSubmission(e.target.value)}
          />
          {codingFeedback ? <p className="text-sm text-white/80">Score: {codingFeedback.score ?? 0} | Passed: {String(codingFeedback.passed ?? false)}</p> : null}
        </section>

        <section className="glass-card space-y-4 lg:col-span-2">
          <div className="flex items-center gap-2"><BarChart3 size={18} /><h3 className="font-black">Performance Tracking</h3></div>
          <button className="btn-primary" onClick={loadPerformance} disabled={isLoading === 'performance'}>Load Performance</button>
          {performance ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <p className="font-bold mb-2">Weak Topics</p>
                {(performance.weak_topics || []).map((w: WeakTopicItem, idx: number) => <p key={idx} className="text-white/70">{w._id}: {Math.round(w.avg_score || 0)}%</p>)}
              </div>
              <div>
                <p className="font-bold mb-2">Recent Scores</p>
                {(performance.history || []).map((h: PerformanceHistoryItem, idx: number) => <p key={idx} className="text-white/70">{h.date} - {h.topic}: {Math.round(h.score)}%</p>)}
              </div>
            </div>
          ) : null}
        </section>
      </div>
    </div>
  );
};

export default AiTutorLab;

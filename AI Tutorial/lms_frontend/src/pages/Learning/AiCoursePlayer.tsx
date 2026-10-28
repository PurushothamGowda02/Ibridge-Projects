import { useMemo, useState } from 'react';
import { lmsApi, STORAGE_KEYS } from '../../services/lmsApi';
import type { GeneratedCourseResponse, GeneratedCourseModule, GeneratedTestResponse, VideoItem } from '../../services/apiTypes';
import { useToast } from '../../components/ToastProvider';
import { getErrorMessage } from '../../utils/errors';

const AiCoursePlayer = () => {
  const toast = useToast();
  const course = useMemo<GeneratedCourseResponse | null>(() => {
    const raw = localStorage.getItem(STORAGE_KEYS.aiGeneratedCourse);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as GeneratedCourseResponse;
    } catch {
      return null;
    }
  }, []);

  const [activeModuleIndex, setActiveModuleIndex] = useState(0);
  const [activeVideoUrl, setActiveVideoUrl] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<GeneratedTestResponse | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [quizScore, setQuizScore] = useState<{ correct: number; total: number; percent: number } | null>(null);
  const [isLoading, setIsLoading] = useState<string | null>(null);

  const getYouTubeId = (url?: string) => {
    if (!url) return null;
    const match = url.match(/(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{11})/);
    return match?.[1] || null;
  };

  if (!course || !course.modules || !Array.isArray(course.modules)) {
    return <div className="max-w-4xl mx-auto py-20 text-center text-white/50">No AI-generated course found. Generate one from AI Tutor Lab.</div>;
  }

  const module = course.modules[activeModuleIndex] as GeneratedCourseModule;

  const generateModuleTest = async () => {
    try {
      setIsLoading('test');
      const res = await lmsApi.generateTest({
        topic: module.title,
        difficulty: 'Intermediate',
        type: 'mixed',
      });
      setTestResult(res.data);
      setSelectedAnswers({});
      setQuizScore(null);
    } catch (err) {
      console.error('Generate test failed', err);
      toast.error(getErrorMessage(err, 'Failed to generate module test.'));
    } finally {
      setIsLoading(null);
    }
  };

  const submitQuiz = () => {
    if (!testResult?.questions?.length) return;
    const mcqs = testResult.questions.filter((q) => q.type === 'mcq');
    const total = mcqs.length;
    if (total === 0) {
      toast.info('No MCQ questions available for scoring in this test.');
      return;
    }
    let correct = 0;
    mcqs.forEach((q, idx) => {
      const picked = selectedAnswers[idx];
      if (picked && q.correct_answer && picked === q.correct_answer) correct += 1;
    });
    const percent = Math.round((correct / total) * 100);
    setQuizScore({ correct, total, percent });
    toast.success(`Quiz submitted: ${correct}/${total} correct`);
    void lmsApi.submitTestResult({ topic: module.title, score: correct, total });
  };

  const saveCourse = async () => {
    try {
      setIsLoading('save');
      await lmsApi.saveCourse({ course });
      toast.success('Course saved. You can continue later from My Courses.');
    } catch (err) {
      toast.error(getErrorMessage(err, 'Failed to save course.'));
    } finally {
      setIsLoading(null);
    }
  };

  const joinCourse = async () => {
    if (!quizScore) {
      toast.info('Complete and submit pre-course test first.');
      return;
    }
    if (quizScore.percent < 60) {
      toast.error('Minimum 60% required in pre-course test to join this course.');
      return;
    }
    try {
      setIsLoading('join');
      await lmsApi.joinCourse({ course, pretest: { correct: quizScore.correct, total: quizScore.total } });
      toast.success('Joined successfully. Course is now in My Courses.');
    } catch (err) {
      toast.error(getErrorMessage(err, 'Failed to join course.'));
    } finally {
      setIsLoading(null);
    }
  };

  const completeModule = async () => {
    try {
      setIsLoading('complete');
      const score = Math.min(100, Math.max(0, Number(prompt('Enter your module test score (0-100):', '70') || 0)));
      const res = await lmsApi.completeModule({
        course_title: course.title || 'AI Course',
        module_title: module.title,
        score,
        pass_mark: 60,
      });
      toast.info(`Module status: ${res.data.passed ? 'Passed' : 'Retake required'}`);
    } catch (err) {
      console.error('Module completion failed', err);
      toast.error(getErrorMessage(err, 'Failed to complete module.'));
    } finally {
      setIsLoading(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto pb-20 grid grid-cols-1 lg:grid-cols-3 gap-8">
      <aside className="glass-card lg:col-span-1 space-y-3 h-fit sticky top-6">
        <h2 className="text-xl font-black">{course.title || 'AI Course'}</h2>
        {course.modules.map((m: GeneratedCourseModule, idx: number) => (
          <button
            key={idx}
            onClick={() => setActiveModuleIndex(idx)}
            className={`w-full text-left p-3 rounded-xl transition ${idx === activeModuleIndex ? 'bg-primary/20 border border-primary/30' : 'bg-white/5 hover:bg-white/10'}`}
          >
            <p className="font-bold text-sm">Module {idx + 1}</p>
            <p className="text-xs text-white/70">{m.title}</p>
          </button>
        ))}
      </aside>

      <main className="glass-card lg:col-span-2 space-y-6">
        <div>
          <p className="text-xs text-white/40 uppercase tracking-widest">Current Module</p>
          <h3 className="text-2xl font-black mt-1">{module.title}</h3>
          <p className="text-white/60 mt-2">{module.description || 'AI-generated learning module.'}</p>
        </div>

        <div className="space-y-3">
          <p className="text-sm font-bold">Curated Videos</p>
          {(module.videos || []).length === 0 ? (
            <p className="text-white/40 text-sm">No videos available for this module.</p>
          ) : (
            (module.videos || []).map((v: VideoItem) => (
              <button
                type="button"
                key={v.id}
                onClick={() => setActiveVideoUrl(v.link)}
                className="block w-full text-left p-3 rounded-xl bg-white/5 hover:bg-white/10"
              >
                <p className="font-semibold">{v.title}</p>
                <p className="text-xs text-white/50 mt-1">Quality score: {v.quality_score || 0}</p>
              </button>
            ))
          )}
          {activeVideoUrl && getYouTubeId(activeVideoUrl) ? (
            <iframe
              className="w-full aspect-video rounded-xl mt-2"
              src={`https://www.youtube.com/embed/${getYouTubeId(activeVideoUrl)}?autoplay=1&rel=0`}
              title="Course video player"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : null}
        </div>

        <div className="flex flex-wrap gap-3">
          <button className="btn-primary" onClick={generateModuleTest} disabled={isLoading === 'test'}>
            {isLoading === 'test' ? 'Generating...' : 'Generate Module Test'}
          </button>
          <button className="btn-primary bg-white/10 hover:bg-white/20" onClick={saveCourse} disabled={isLoading === 'save'}>
            {isLoading === 'save' ? 'Saving...' : 'Save Course'}
          </button>
          <button className="btn-primary" onClick={joinCourse} disabled={isLoading === 'join'}>
            {isLoading === 'join' ? 'Joining...' : 'Join Course (After Test)'}
          </button>
          <button className="btn-primary bg-white/10 hover:bg-white/20" onClick={completeModule} disabled={isLoading === 'complete'}>
            {isLoading === 'complete' ? 'Saving...' : 'Mark Module Complete'}
          </button>
        </div>

        {testResult?.questions?.length ? (
          <div className="bg-white/5 rounded-xl p-4">
            <p className="font-bold">Generated Test: {testResult.title || module.title}</p>
            <p className="text-sm text-white/70 mt-1">Questions: {testResult.questions.length}</p>
            <div className="mt-4 space-y-3">
              {testResult.questions.map((q, idx) => (
                <div key={idx} className="rounded-lg bg-white/5 p-3">
                  <p className="text-sm font-semibold">
                    Q{idx + 1}. {q.question || q.task || 'Question'}
                  </p>
                  {q.type === 'mcq' && q.options?.length ? (
                    <div className="mt-2 text-sm text-white/75 space-y-2">
                      {q.options.map((opt, optIdx) => {
                        const optionLetter = String.fromCharCode(65 + optIdx);
                        return (
                          <label key={optIdx} className="flex items-center gap-2 cursor-pointer">
                            <input
                              type="radio"
                              name={`q-${idx}`}
                              value={opt}
                              checked={selectedAnswers[idx] === opt}
                              onChange={() => setSelectedAnswers((prev) => ({ ...prev, [idx]: opt }))}
                            />
                            <span>{optionLetter}. {opt}</span>
                          </label>
                        );
                      })}
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
            <div className="mt-4 flex flex-wrap gap-3">
              <button className="btn-primary" onClick={submitQuiz}>
                Submit Answers
              </button>
              {quizScore ? (
                <p className="text-sm text-white/80 self-center">
                  Result: {quizScore.correct}/{quizScore.total} correct ({quizScore.percent}%)
                </p>
              ) : null}
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
};

export default AiCoursePlayer;

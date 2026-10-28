import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { lmsApi } from '../../services/lmsApi';
import type { GeneratedTestResponse } from '../../services/apiTypes';
import { useToast } from '../../components/ToastProvider';
import { getErrorMessage } from '../../utils/errors';

type CourseType = {
  id: string;
  title: string;
  subject: string;
  topic: string;
  difficulty: string;
  description: string;
};

const COURSE_TYPES: CourseType[] = [
  {
    id: 'web-dev',
    title: 'Web Development',
    subject: 'Programming',
    topic: 'Frontend and Backend Web Development',
    difficulty: 'Beginner',
    description: 'Build websites and APIs with modern full-stack workflows.',
  },
  {
    id: 'data-science',
    title: 'Data Science',
    subject: 'Data',
    topic: 'Data Science and Machine Learning',
    difficulty: 'Intermediate',
    description: 'Learn data analysis, modeling, and practical ML pipelines.',
  },
  {
    id: 'dsa',
    title: 'Data Structures and Algorithms',
    subject: 'Programming',
    topic: 'Data Structures and Algorithms',
    difficulty: 'Intermediate',
    description: 'Master core interview-focused problem solving techniques.',
  },
  {
    id: 'cloud',
    title: 'Cloud and DevOps',
    subject: 'Infrastructure',
    topic: 'Cloud Computing and DevOps',
    difficulty: 'Intermediate',
    description: 'Deploy, scale, and automate applications in cloud platforms.',
  },
];

const PreEligibility = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const [selectedTypeId, setSelectedTypeId] = useState<string>(COURSE_TYPES[0].id);
  const [isLoading, setIsLoading] = useState<string | null>(null);
  const [testData, setTestData] = useState<GeneratedTestResponse | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [score, setScore] = useState<{ correct: number; total: number; percent: number } | null>(null);

  const selectedType = useMemo(
    () => COURSE_TYPES.find((c) => c.id === selectedTypeId) || COURSE_TYPES[0],
    [selectedTypeId],
  );

  const generatePreTest = async () => {
    try {
      setIsLoading('test');
      const res = await lmsApi.generateTest({
        topic: selectedType.topic,
        difficulty: selectedType.difficulty,
        type: 'mcq',
      });
      setTestData(res.data);
      setSelectedAnswers({});
      setScore(null);
    } catch (err) {
      toast.error(getErrorMessage(err, 'Failed to generate pre-eligibility test.'));
    } finally {
      setIsLoading(null);
    }
  };

  const submitPreTest = async () => {
    if (!testData?.questions?.length) return;
    const mcqs = testData.questions.filter((q) => q.type === 'mcq');
    const total = mcqs.length;
    if (total === 0) {
      toast.info('No MCQ questions available for eligibility scoring.');
      return;
    }
    let correct = 0;
    mcqs.forEach((q, idx) => {
      if (selectedAnswers[idx] && q.correct_answer && selectedAnswers[idx] === q.correct_answer) {
        correct += 1;
      }
    });
    const percent = Math.round((correct / total) * 100);
    setScore({ correct, total, percent });
    await lmsApi.submitTestResult({ topic: `${selectedType.title} Pre-Eligibility`, score: correct, total });
    if (percent >= 60) {
      toast.success(`Passed pre-eligibility test (${percent}%). You can enroll now.`);
    } else {
      toast.error(`Score ${percent}%. Minimum 60% required to enroll.`);
    }
  };

  const enrollCourse = async () => {
    if (!score || score.percent < 60) {
      toast.error('Pass the pre-eligibility test first (minimum 60%).');
      return;
    }
    try {
      setIsLoading('enroll');
      const courseRes = await lmsApi.generateCourse({ topic: selectedType.topic });
      const course = courseRes.data;
      await lmsApi.joinCourse({
        course,
        pretest: { correct: score.correct, total: score.total },
      });
      toast.success('Enrollment successful. Course added to My Courses.');
      navigate('/my-courses');
    } catch (err) {
      toast.error(getErrorMessage(err, 'Failed to enroll in course.'));
    } finally {
      setIsLoading(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto pb-20 space-y-8">
      <div>
        <h2 className="text-4xl font-extrabold tracking-tight">
          Pre-Eligibility <span className="text-primary italic">Test</span>
        </h2>
        <p className="text-white/40 font-medium">
          Choose a course type, pass the eligibility test, then enroll.
        </p>
      </div>

      <section className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {COURSE_TYPES.map((c) => (
          <button
            key={c.id}
            type="button"
            onClick={() => setSelectedTypeId(c.id)}
            className={`p-4 rounded-xl text-left transition ${
              c.id === selectedTypeId ? 'bg-primary/20 border border-primary/40' : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            <p className="font-bold">{c.title}</p>
            <p className="text-xs text-white/50 mt-1">{c.description}</p>
          </button>
        ))}
      </section>

      <section className="glass-card space-y-4">
        <div className="flex flex-wrap gap-3">
          <button className="btn-primary" onClick={generatePreTest} disabled={isLoading === 'test'}>
            {isLoading === 'test' ? 'Generating...' : 'Generate Pre-Eligibility Test'}
          </button>
          <button className="btn-primary bg-white/10 hover:bg-white/20" onClick={submitPreTest} disabled={!testData}>
            Submit Test
          </button>
          <button className="btn-primary" onClick={enrollCourse} disabled={isLoading === 'enroll'}>
            {isLoading === 'enroll' ? 'Enrolling...' : 'Enroll Course'}
          </button>
        </div>

        {score ? (
          <p className="text-sm text-white/80">
            Result: {score.correct}/{score.total} correct ({score.percent}%)
          </p>
        ) : null}

        {testData?.questions?.length ? (
          <div className="space-y-3">
            {testData.questions
              .filter((q) => q.type === 'mcq')
              .map((q, idx) => (
                <div key={idx} className="rounded-lg bg-white/5 p-3">
                  <p className="text-sm font-semibold">Q{idx + 1}. {q.question || 'Question'}</p>
                  <div className="mt-2 text-sm text-white/75 space-y-2">
                    {(q.options || []).map((opt, optIdx) => (
                      <label key={optIdx} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="radio"
                          name={`pre-q-${idx}`}
                          value={opt}
                          checked={selectedAnswers[idx] === opt}
                          onChange={() => setSelectedAnswers((prev) => ({ ...prev, [idx]: opt }))}
                        />
                        <span>{String.fromCharCode(65 + optIdx)}. {opt}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
          </div>
        ) : (
          <p className="text-white/40 text-sm">Generate a test to start eligibility evaluation.</p>
        )}
      </section>
    </div>
  );
};

export default PreEligibility;


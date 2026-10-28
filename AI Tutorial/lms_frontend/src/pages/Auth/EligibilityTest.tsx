import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Loader, CheckCircle, XCircle, Clock, Award } from 'lucide-react';
import axios from 'axios';

interface Question {
  id: number;
  question: string;
  options: string[];
  correct_answer: string;
}

const EligibilityTest = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [testStarted, setTestStarted] = useState(false);
  const [testSubmitted, setTestSubmitted] = useState(false);
  const [result, setResult] = useState<{ passed: boolean; score: number; total: number; percentage: number } | null>(null);
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes
  const navigate = useNavigate();

  // Sample questions (in production, fetch from backend)
  const sampleQuestions: Question[] = [
    {
      id: 1,
      question: "What is the primary purpose of a Learning Management System (LMS)?",
      options: [
        "To manage student attendance only",
        "To deliver, track, and manage training and education",
        "To create social media content",
        "To design websites"
      ],
      correct_answer: "To deliver, track, and manage training and education"
    },
    {
      id: 2,
      question: "Which of the following is a benefit of online learning?",
      options: [
        "Limited access to resources",
        "Fixed learning schedule",
        "Flexibility in time and location",
        "No interaction with instructors"
      ],
      correct_answer: "Flexibility in time and location"
    },
    {
      id: 3,
      question: "What does AI stand for in the context of education technology?",
      options: [
        "Automated Intelligence",
        "Artificial Intelligence",
        "Advanced Integration",
        "Academic Information"
      ],
      correct_answer: "Artificial Intelligence"
    },
    {
      id: 4,
      question: "What is the minimum passing score for this eligibility test?",
      options: [
        "50%",
        "60%",
        "70%",
        "80%"
      ],
      correct_answer: "60%"
    },
    {
      id: 5,
      question: "Which learning approach allows students to learn at their own pace?",
      options: [
        "Synchronous learning",
        "Self-paced learning",
        "Classroom learning",
        "Group learning"
      ],
      correct_answer: "Self-paced learning"
    }
  ];

  useEffect(() => {
    if (testStarted && !testSubmitted && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [testStarted, testSubmitted, timeLeft]);

  const startTest = () => {
    setQuestions(sampleQuestions);
    setTestStarted(true);
    setTimeLeft(600); // 10 minutes
  };

  const handleAnswerSelect = (answer: string) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [currentQuestion]: answer
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    
    // Calculate score
    let correct = 0;
    questions.forEach((q, idx) => {
      if (selectedAnswers[idx] === q.correct_answer) {
        correct++;
      }
    });

    const total = questions.length;
    const percentage = Math.round((correct / total) * 100);
    const passed = percentage >= 60;

    try {
      // Submit to backend
      const token = localStorage.getItem('token');
      await axios.post(
        '/api/v1/auth/eligibility-test/submit',
        {
          score: correct,
          total: total,
          answers: selectedAnswers
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setResult({ passed, score: correct, total, percentage });
      setTestSubmitted(true);
    } catch (error) {
      console.error('Failed to submit test:', error);
      setResult({ passed, score: correct, total, percentage });
      setTestSubmitted(true);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!testStarted) {
    return (
      <div className="min-h-screen bg-[radial-gradient(at_0%_0%,rgba(59,130,246,0.05)_0px,transparent_50%),radial-gradient(at_100%_100%,rgba(168,85,247,0.05)_0px,transparent_50%)]">
        <div className="border-b border-white/10 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-2">
            <BookOpen className="text-primary" size={28} />
            <span className="text-xl font-bold">AI Tutorial LMS</span>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="glass-card text-center">
            <div className="bg-primary/20 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
              <Award className="text-primary" size={40} />
            </div>
            
            <h1 className="text-4xl font-extrabold mb-4">
              Pre-Eligibility <span className="text-primary">Test</span>
            </h1>
            
            <p className="text-white/60 text-lg mb-8 max-w-2xl mx-auto">
              Before accessing our tutorials, you need to pass a simple eligibility test to ensure you're ready for the learning journey ahead.
            </p>

            <div className="bg-white/5 rounded-xl p-6 mb-8 text-left max-w-2xl mx-auto">
              <h3 className="font-bold text-lg mb-4">Test Instructions:</h3>
              <ul className="space-y-2 text-white/70">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Total Questions: <strong className="text-white">5</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Time Limit: <strong className="text-white">10 minutes</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Passing Score: <strong className="text-white">60% (3 out of 5 correct)</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>You can navigate between questions before submitting</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Once submitted, you cannot retake the test</span>
                </li>
              </ul>
            </div>

            <button
              onClick={startTest}
              className="btn-primary text-lg px-8 py-4"
            >
              Start Eligibility Test
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (testSubmitted && result) {
    return (
      <div className="min-h-screen bg-[radial-gradient(at_0%_0%,rgba(59,130,246,0.05)_0px,transparent_50%),radial-gradient(at_100%_100%,rgba(168,85,247,0.05)_0px,transparent_50%)]">
        <div className="border-b border-white/10 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-2">
            <BookOpen className="text-primary" size={28} />
            <span className="text-xl font-bold">AI Tutorial LMS</span>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="glass-card text-center">
            <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 ${result.passed ? 'bg-green-500/20' : 'bg-red-500/20'}`}>
              {result.passed ? (
                <CheckCircle className="text-green-500" size={48} />
              ) : (
                <XCircle className="text-red-500" size={48} />
              )}
            </div>

            <h2 className="text-3xl font-bold mb-4">
              {result.passed ? 'Congratulations! 🎉' : 'Test Not Passed'}
            </h2>

            <p className="text-white/60 text-lg mb-8">
              {result.passed
                ? 'You have successfully passed the eligibility test!'
                : 'You need at least 60% to pass. Please contact support for assistance.'}
            </p>

            <div className="bg-white/5 rounded-xl p-8 mb-8 max-w-md mx-auto">
              <div className="text-6xl font-bold text-primary mb-2">{result.percentage}%</div>
              <div className="text-white/60">
                {result.score} out of {result.total} correct answers
              </div>
            </div>

            {result.passed ? (
              <button
                onClick={() => navigate('/dashboard')}
                className="btn-primary text-lg px-8 py-4"
              >
                Continue to Dashboard
              </button>
            ) : (
              <button
                onClick={() => navigate('/login')}
                className="btn-primary bg-white/10 hover:bg-white/20 text-lg px-8 py-4"
              >
                Back to Login
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-[radial-gradient(at_0%_0%,rgba(59,130,246,0.05)_0px,transparent_50%),radial-gradient(at_100%_100%,rgba(168,85,247,0.05)_0px,transparent_50%)]">
      <div className="border-b border-white/10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="text-primary" size={28} />
            <span className="text-xl font-bold">Eligibility Test</span>
          </div>
          <div className="flex items-center gap-2 text-primary font-bold">
            <Clock size={20} />
            <span>{formatTime(timeLeft)}</span>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between text-sm text-white/60 mb-2">
            <span>Question {currentQuestion + 1} of {questions.length}</span>
            <span>{Math.round(progress)}% Complete</span>
          </div>
          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-primary transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Question Card */}
        <div className="glass-card mb-6">
          <h3 className="text-2xl font-bold mb-6">{currentQ.question}</h3>

          <div className="space-y-3">
            {currentQ.options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => handleAnswerSelect(option)}
                className={`w-full text-left p-4 rounded-xl transition ${
                  selectedAnswers[currentQuestion] === option
                    ? 'bg-primary/20 border-2 border-primary'
                    : 'bg-white/5 hover:bg-white/10 border-2 border-transparent'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    selectedAnswers[currentQuestion] === option
                      ? 'border-primary bg-primary'
                      : 'border-white/30'
                  }`}>
                    {selectedAnswers[currentQuestion] === option && (
                      <div className="w-2 h-2 bg-white rounded-full" />
                    )}
                  </div>
                  <span>{option}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center">
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="btn-primary bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          <div className="flex gap-2">
            {questions.map((_, idx) => (
              <button
                key={idx}
                onClick={() => setCurrentQuestion(idx)}
                className={`w-8 h-8 rounded-full text-sm font-bold transition ${
                  idx === currentQuestion
                    ? 'bg-primary text-white'
                    : selectedAnswers[idx]
                    ? 'bg-green-500/20 text-green-500'
                    : 'bg-white/10 text-white/50'
                }`}
              >
                {idx + 1}
              </button>
            ))}
          </div>

          {currentQuestion === questions.length - 1 ? (
            <button
              onClick={handleSubmit}
              disabled={isLoading || Object.keys(selectedAnswers).length !== questions.length}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader className="animate-spin" size={20} />
                  <span>Submitting...</span>
                </>
              ) : (
                'Submit Test'
              )}
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="btn-primary"
            >
              Next
            </button>
          )}
        </div>

        {Object.keys(selectedAnswers).length !== questions.length && (
          <p className="text-center text-yellow-500 text-sm mt-4">
            Please answer all questions before submitting
          </p>
        )}
      </div>
    </div>
  );
};

export default EligibilityTest;

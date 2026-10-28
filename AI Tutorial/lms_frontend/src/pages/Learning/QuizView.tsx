import { useState, useEffect, useCallback } from 'react';
import type { FC } from 'react';
import { 
  ChevronRight, ChevronLeft, 
  Timer, Award, RefreshCw 
} from 'lucide-react';
import { legacyApi } from '../../services/legacyApi';
import type { LegacyQuizAttemptResponse, LegacyQuizResponse } from '../../services/apiTypes';

interface QuizViewProps {
  lessonId: string;
  courseId: string;
  onComplete: (score: number) => void;
}

interface QuizOption {
  text: string;
}

interface QuizQuestion {
  text: string;
  options: QuizOption[];
}

const QuizView: FC<QuizViewProps> = ({ lessonId, courseId, onComplete }) => {
  const [quiz, setQuiz] = useState<LegacyQuizResponse | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [results, setResults] = useState<LegacyQuizAttemptResponse | null>(null);

  const fetchQuiz = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await legacyApi.getQuiz(lessonId);
      setQuiz(response.data);
      setResults(null);
      setSelectedAnswers({});
      setCurrentQuestion(0);
    } catch (err) {
      console.error("Failed to fetch quiz", err);
    } finally {
      setIsLoading(false);
    }
  }, [lessonId]);

  const handleSelect = (optionIdx: number) => {
    setSelectedAnswers({ ...selectedAnswers, [currentQuestion]: optionIdx });
  };

  const submitQuiz = async () => {
    setIsSubmitting(true);
    try {
      const response = await legacyApi.submitQuizAttempt({
        lesson_id: lessonId,
        course_id: courseId,
        answers: selectedAnswers
      });
      setResults(response.data);
      onComplete(response.data.percent);
    } catch (err) {
      console.error("Failed to submit quiz", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  useEffect(() => {
    fetchQuiz();
  }, [fetchQuiz]);

  if (isLoading) return <div className="p-20 text-center text-white/40">Loading Assessment...</div>;
  if (!quiz) return <div className="p-20 text-center text-white/40">No quiz available for this lesson.</div>;

  if (results) {
    return (
      <div className="max-w-2xl mx-auto py-20 text-center animate-in fade-in zoom-in duration-500">
        <div className="bg-primary/20 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-8 shadow-[0_0_50px_rgba(59,130,246,0.3)]">
          <Award className="text-primary" size={48} />
        </div>
        <h2 className="text-4xl font-black mb-4 tracking-tight">Quiz <span className="text-primary italic">Complete!</span></h2>
        <p className="text-white/40 mb-10 font-bold uppercase tracking-widest text-sm">Assessment Results</p>
        
        <div className="grid grid-cols-2 gap-8 mb-12">
           <div className="glass-card p-8 border-l-4 border-l-primary">
              <p className="text-3xl font-black mb-1">{results.score}/{results.total}</p>
              <p className="text-[10px] font-black uppercase tracking-widest text-white/40">Points Earned</p>
           </div>
           <div className="glass-card p-8 border-l-4 border-l-green-500">
              <p className="text-3xl font-black mb-1 text-green-500">{results.percent}%</p>
              <p className="text-[10px] font-black uppercase tracking-widest text-white/40">Final Score</p>
           </div>
        </div>

        <div className="flex gap-4">
           <button onClick={fetchQuiz} className="btn-primary bg-white/5 hover:bg-white/10 flex-1 flex items-center justify-center gap-2">
             <RefreshCw size={18} /> Retake Quiz
           </button>
           <button className="btn-primary flex-1">
             Continue Course
           </button>
        </div>
      </div>
    );
  }

  const question = quiz.questions[currentQuestion] as QuizQuestion;

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <div className="flex items-center justify-between mb-12">
         <div>
            <span className="text-[10px] font-black uppercase tracking-widest text-primary mb-2 block">Question {currentQuestion + 1} of {quiz.questions.length}</span>
            <h3 className="text-2xl font-black tracking-tight">{quiz.title}</h3>
         </div>
         <div className="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-xl border border-white/5">
            <Timer size={16} className="text-white/40" />
            <span className="text-sm font-bold text-white/60 tracking-tighter">12:00</span>
         </div>
      </div>

      <div className="glass-card mb-10 p-10 bg-bg-secondary/40">
         <p className="text-xl font-bold leading-relaxed mb-10">{question.text}</p>
         
         <div className="space-y-4">
            {question.options.map((option: QuizOption, idx: number) => (
              <button 
                key={idx}
                onClick={() => handleSelect(idx)}
                className={`w-full p-5 rounded-2xl border text-left transition-all duration-200 flex items-center justify-between group ${
                  selectedAnswers[currentQuestion] === idx 
                  ? 'bg-primary/20 border-primary shadow-[0_0_30px_rgba(59,130,246,0.1)]' 
                  : 'bg-white/5 border-white/5 hover:border-white/10 hover:bg-white/10'
                }`}
              >
                <div className="flex items-center gap-4">
                   <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold text-xs ${
                     selectedAnswers[currentQuestion] === idx 
                     ? 'bg-primary border-primary text-white' 
                     : 'border-white/10 text-white/40 group-hover:border-white/20'
                   }`}>
                     {String.fromCharCode(65 + idx)}
                   </div>
                   <span className={`font-semibold ${selectedAnswers[currentQuestion] === idx ? 'text-white' : 'text-white/60'}`}>{option.text}</span>
                </div>
                {selectedAnswers[currentQuestion] === idx && <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />}
              </button>
            ))}
         </div>
      </div>

      <div className="flex items-center justify-between">
         <button 
           disabled={currentQuestion === 0}
           onClick={() => setCurrentQuestion(currentQuestion - 1)}
           className="flex items-center gap-2 text-sm font-bold text-white/40 hover:text-white transition-colors disabled:opacity-0"
         >
            <ChevronLeft size={20} /> Previous
         </button>

         {currentQuestion === quiz.questions.length - 1 ? (
           <button 
             onClick={submitQuiz}
             disabled={isSubmitting || selectedAnswers[currentQuestion] === undefined}
             className="btn-primary px-10 shadow-[0_0_30px_rgba(59,130,246,0.3)] disabled:opacity-50"
           >
             {isSubmitting ? 'Submitting...' : 'Complete Assessment'}
           </button>
         ) : (
           <button 
             onClick={() => setCurrentQuestion(currentQuestion + 1)}
             disabled={selectedAnswers[currentQuestion] === undefined}
             className="btn-primary px-10 flex items-center gap-2 group disabled:opacity-50"
           >
             Next Question <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
           </button>
         )}
      </div>
    </div>
  );
};

export default QuizView;

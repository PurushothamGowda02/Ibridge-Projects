import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, Loader2, 
  Play, Save, Trash2 
} from 'lucide-react';
import { legacyApi } from '../../services/legacyApi';
import type { LegacyCourse, LegacyLesson, LegacyModule } from '../../services/apiTypes';
import { useToast } from '../../components/ToastProvider';
import { getErrorMessage } from '../../utils/errors';

const AICreator = () => {
  const toast = useToast();
  const [prompt, setPrompt] = useState('');
  const [difficulty, setDifficulty] = useState('Beginner');
  const [isGenerating, setIsGenerating] = useState(false);
  const [step, setStep] = useState(0); // 0: Idle, 1: AI Prompting, 2: Video Curation, 3: Review
  const [generatedCourse, setGeneratedCourse] = useState<LegacyCourse | null>(null);
  const navigate = useNavigate();
  const reviewedCourse = generatedCourse;

  const handleGenerate = async () => {
    if (!prompt) return;
    
    setIsGenerating(true);
    setStep(1);
    
    try {
      // Step 1: AI Archiving (Implicit in the backend call, but we simulate progress)
      setTimeout(() => setStep(2), 2000);
      
      const response = await legacyApi.generateAiCourse({
        topic: prompt,
        difficulty: difficulty
      });
      
      setGeneratedCourse(response.data);
      setStep(3);
      toast.success('AI masterclass generated.');
    } catch (err) {
      console.error("AI Generation failed", err);
      setStep(0);
      toast.error(getErrorMessage(err, 'AI generation failed.'));
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSave = async () => {
    if (!generatedCourse) return;
    try {
      await legacyApi.createCourse(generatedCourse);
      toast.success('Course deployed successfully.');
      navigate(`/dashboard`);
    } catch (err) {
      console.error("Failed to save AI course", err);
      toast.error(getErrorMessage(err, 'Failed to deploy course.'));
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20">
      <div className="flex items-center gap-4 mb-12">
        <div className="bg-primary/20 p-3 rounded-2xl">
          <Sparkles className="text-primary" size={32} />
        </div>
        <div>
          <h2 className="text-4xl font-extrabold tracking-tight">AI <span className="text-primary italic">Architect</span></h2>
          <p className="text-white/40 font-medium tracking-tight">Generate a masterclass in seconds using advanced AI models.</p>
        </div>
      </div>

      {step < 3 ? (
        <div className="glass-card p-12 bg-bg-secondary/40 border-dashed border-white/10 text-center">
            <div className="max-w-2xl mx-auto space-y-10">
              <div className="space-y-4">
                 <h3 className="text-2xl font-black italic tracking-tighter">What would you like to teach?</h3>
                 <p className="text-white/30">Just enter a subject—from "Theoretical Physics" to "Spanish Cooking"—and we'll build the curriculum.</p>
              </div>

              <div className="relative group">
                <textarea 
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  disabled={isGenerating}
                  placeholder="e.g., A comprehensive guide to Modern Web Security and Hacking"
                  className="input-field w-full min-h-[150px] p-8 text-xl bg-bg-dark border-white/5 focus:border-primary/40 resize-none"
                />
                <div className="absolute top-4 right-4 flex gap-2">
                   {['Beginner', 'Intermediate', 'Advanced'].map(d => (
                     <button 
                       key={d} 
                       onClick={() => setDifficulty(d)}
                       className={`px-4 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                         difficulty === d ? 'bg-primary text-white' : 'bg-white/5 text-white/30 hover:bg-white/10'
                       }`}
                     >
                       {d}
                     </button>
                   ))}
                </div>
              </div>

              <button 
                onClick={handleGenerate}
                disabled={isGenerating || !prompt}
                className="btn-primary w-full py-5 text-lg flex items-center justify-center gap-4 shadow-[0_0_50px_rgba(59,130,246,0.3)] disabled:opacity-50"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="animate-spin" />
                    <span>{step === 1 ? 'Architecting Syllabus...' : 'Curating Best Content...'}</span>
                  </>
                ) : (
                  <>
                    <Sparkles size={24} />
                    <span>Generate Masterclass</span>
                  </>
                )}
              </button>
            </div>
        </div>
      ) : reviewedCourse ? (
        <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
           {/* Review Header */}
           <div className="flex items-center justify-between glass-card bg-primary/10 border-primary/20 p-8">
              <div className="flex items-center gap-6">
                 <div className="bg-primary text-white p-4 rounded-2xl font-black">AI</div>
                 <div>
                    <h3 className="text-2xl font-black leading-none mb-1">{reviewedCourse.title}</h3>
                    <p className="text-white/40 text-sm">{reviewedCourse.description}</p>
                 </div>
              </div>
              <div className="flex gap-4">
                 <button onClick={() => setStep(0)} className="bg-white/5 hover:bg-white/10 p-4 rounded-2xl transition-all">
                    <Trash2 size={20} className="text-white/40" />
                 </button>
                 <button onClick={handleSave} className="bg-primary hover:bg-primary-hover px-8 py-4 rounded-2xl font-black uppercase tracking-widest flex items-center gap-2 shadow-lg">
                    <Save size={20} /> Deploy Course
                 </button>
              </div>
           </div>

           {/* Syllabus Preview */}
           <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {reviewedCourse.modules.map((module: LegacyModule, mIdx: number) => (
                <div key={mIdx} className="glass-card hover:border-primary/20 transition-all group">
                   <div className="flex items-center gap-3 mb-6">
                      <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center font-black text-xs text-white/40 border border-white/5">
                        {mIdx + 1}
                      </div>
                      <h4 className="font-black text-white/80 group-hover:text-primary transition-colors">{module.title}</h4>
                   </div>
                   
                   <div className="space-y-4">
                      {module.lessons.map((lesson: LegacyLesson, lIdx: number) => (
                        <div key={lIdx} className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5">
                           {lesson.thumbnail ? (
                             <div className="w-24 aspect-video rounded-lg overflow-hidden shrink-0 border border-white/10">
                                <img src={lesson.thumbnail} alt="" className="w-full h-full object-cover" />
                             </div>
                           ) : (
                             <div className="w-24 aspect-video rounded-lg bg-bg-dark flex items-center justify-center shrink-0 border border-white/10">
                                <Play size={20} className="text-white/20" />
                             </div>
                           )}
                           <div className="flex-1 overflow-hidden">
                              <p className="text-xs font-black truncate">{lesson.title}</p>
                              <div className="flex items-center gap-4 mt-2">
                                 <span className="text-[9px] font-black uppercase tracking-widest text-primary bg-primary/10 px-2 py-0.5 rounded border border-primary/20">{lesson.type}</span>
                                 <span className="text-[9px] font-black uppercase tracking-widest text-white/20">Lesson {lIdx + 1}</span>
                              </div>
                           </div>
                        </div>
                      ))}
                   </div>
                </div>
              ))}
           </div>
        </div>
      ) : (
        <div className="glass-card p-12 text-center text-white/50">No generated course to review yet.</div>
      )}
    </div>
  );
};

export default AICreator;

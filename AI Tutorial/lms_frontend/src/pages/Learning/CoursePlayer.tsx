import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ChevronLeft, CheckCircle, Circle, Play, FileText, 
  ArrowRight, ArrowLeft, Menu, X, Youtube, HelpCircle 
} from 'lucide-react';
import QuizView from './QuizView';
import { legacyApi } from '../../services/legacyApi';
import type { LegacyCourse, LegacyLesson, LegacyModule, LegacyResourceItem } from '../../services/apiTypes';

const getYouTubeId = (url: string) => {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
};

const CoursePlayer = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState<LegacyCourse | null>(null);
  const [activeLesson, setActiveLesson] = useState<LegacyLesson | null>(null);
  const [progress, setProgress] = useState<Record<string, boolean>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const activeLessonId = activeLesson?.id;

  const fetchCourseData = useCallback(async () => {
    try {
      const response = await legacyApi.getCourseById(courseId || '');
      setCourse(response.data);
      if (response.data.modules.length > 0 && response.data.modules[0].lessons.length > 0) {
        setActiveLesson(response.data.modules[0].lessons[0]);
      }
    } catch (err) {
      console.error("Failed to fetch course detail", err);
    } finally {
      setIsLoading(false);
    }
  }, [courseId]);

  const fetchProgress = useCallback(async () => {
    try {
      const response = await legacyApi.getProgress(courseId || '');
      setProgress(response.data);
    } catch (err) {
      console.error("Failed to fetch progress", err);
    }
  }, [courseId]);

  const toggleComplete = async (lessonId: string) => {
    try {
      const response = await legacyApi.toggleLessonProgress(lessonId, courseId || '');
      setProgress(prev => ({ ...prev, [lessonId]: response.data.is_completed }));
    } catch (err) {
      console.error("Failed to toggle completion", err);
    }
  };

  useEffect(() => {
    fetchCourseData();
    fetchProgress();
  }, [fetchCourseData, fetchProgress]);

  if (isLoading) return <div className="h-screen flex items-center justify-center text-primary font-bold">Initializing Classroom...</div>;
  if (!course) return <div className="p-20 text-center">Course not found.</div>;

  return (
    <div className="flex h-screen bg-bg-dark overflow-hidden">
      {/* Sidebar - Course Curriculum */}
      <aside className={`${isSidebarOpen ? 'w-96' : 'w-0'} bg-bg-secondary border-r border-white/5 transition-all duration-300 flex flex-col overflow-hidden`}>
        <div className="p-6 border-b border-white/5 flex items-center justify-between">
          <button onClick={() => navigate('/my-courses')} className="text-white/40 hover:text-white transition-colors flex items-center gap-2 text-xs font-bold uppercase tracking-widest">
            <ChevronLeft size={16} /> Dashboard
          </button>
          <button onClick={() => setIsSidebarOpen(false)} className="text-white/20 hover:text-white transition-colors lg:hidden">
            <X size={20} />
          </button>
        </div>

        <div className="p-6 overflow-y-auto flex-1 custom-scrollbar">
          <h2 className="text-xl font-black mb-8 leading-tight">{course.title}</h2>
          
          <div className="space-y-10">
            {course.modules.map((module: LegacyModule, mIdx: number) => (
              <div key={mIdx}>
                <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-white/30 mb-4">{module.title}</h3>
                <div className="space-y-1">
                  {module.lessons.map((lesson: LegacyLesson, lIdx: number) => {
                    const isCompleted = progress[lesson.id];
                    const isActive = activeLesson?.id === lesson.id;
                    
                    return (
                      <button 
                        key={lIdx}
                        onClick={() => setActiveLesson(lesson)}
                        className={`w-full text-left p-4 rounded-xl flex items-center gap-4 transition-all duration-200 group ${
                          isActive 
                          ? 'bg-primary/10 border border-primary/20 text-white' 
                          : 'text-white/50 hover:bg-white/5'
                        }`}
                      >
                         <div className="shrink-0">
                           {isCompleted ? (
                             <CheckCircle size={18} className="text-green-500" />
                           ) : (
                             isActive ? <Play size={18} className="text-primary" /> : <div className="w-[18px] h-[18px] rounded-full border-2 border-white/10 group-hover:border-primary/50 transition-colors" />
                           )}
                         </div>
                         <div className="flex-1 overflow-hidden">
                            <p className={`text-sm font-bold truncate ${isActive ? 'text-white' : 'group-hover:text-white'}`}>{lesson.title}</p>
                            <div className="flex items-center gap-2 mt-1">
                               {lesson.type === 'video' ? <Youtube size={12} className="text-white/20" /> : lesson.type === 'quiz' ? <HelpCircle size={12} className="text-white/20" /> : <FileText size={12} className="text-white/20" />}
                               <span className="text-[10px] font-bold uppercase tracking-widest text-white/20">Lesson {lIdx + 1}</span>
                            </div>
                         </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      </aside>

      {/* Main Content - Video Player */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden relative">
        {/* Top Navbar */}
        <header className="px-8 py-4 bg-bg-dark border-b border-white/5 flex items-center justify-between sticky top-0 z-10">
           {!isSidebarOpen && (
             <button onClick={() => setIsSidebarOpen(true)} className="p-2 -ml-2 text-white/40 hover:text-white transition-colors">
                <Menu size={20} />
             </button>
           )}
           <div className="flex items-center gap-3">
             <span className="text-[10px] font-black uppercase tracking-widest bg-white/5 text-white/40 px-3 py-1 rounded border border-white/5">{activeLesson?.type}</span>
             <h4 className="text-sm font-black truncate max-w-lg">{activeLesson?.title}</h4>
           </div>
           
           <button 
             onClick={() => activeLesson && toggleComplete(activeLesson.id)}
             className={`flex items-center gap-2 px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all duration-300 ${
               activeLessonId && progress[activeLessonId]
               ? 'bg-green-500/10 text-green-500 border border-green-500/20' 
               : 'bg-white/5 text-white/40 hover:bg-white/10 hover:text-white'
             }`}
             disabled={activeLesson?.type === 'quiz'}
           >
             {activeLessonId && progress[activeLessonId] ? <CheckCircle size={16} /> : <Circle size={16} />}
             {activeLessonId && progress[activeLessonId] ? 'Completed' : 'Mark as Done'}
           </button>
        </header>

        {/* Video Area */}
        <div className="flex-1 p-8 overflow-y-auto custom-scrollbar">
           <div className="max-w-5xl mx-auto space-y-12">
              <div className={`aspect-video bg-black rounded-3xl overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)] border border-white/5 ${activeLesson?.type === 'quiz' ? 'h-auto min-h-[600px] bg-bg-dark border-none shadow-none' : ''}`}>
                 {activeLesson?.type === 'video' && activeLesson?.youtube_url ? (
                   <iframe
                     width="100%"
                     height="100%"
                     src={`https://www.youtube.com/embed/${getYouTubeId(activeLesson.youtube_url)}?autoplay=0&rel=0`}
                     title={activeLesson.title}
                     frameBorder="0"
                     allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                     allowFullScreen
                   ></iframe>
                 ) : activeLesson?.type === 'quiz' ? (
                    <QuizView 
                      lessonId={activeLesson.id} 
                      courseId={courseId || ''} 
                      onComplete={() => fetchProgress()} 
                    />
                 ) : (
                   <div className="w-full h-full flex flex-col items-center justify-center gap-6 p-20 text-center">
                      <FileText size={48} className="text-primary/20" />
                      <div className="prose prose-invert max-w-none text-left p-10 glass-card bg-bg-secondary w-full">
                         <h2 className="text-2xl font-black mb-4">Reading Material</h2>
                         <p className="text-white/60 leading-relaxed">{activeLesson?.content || 'Study the provided resources for this lesson.'}</p>
                      </div>
                   </div>
                 )}
              </div>

              {/* Lesson Description & Resources */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 pb-20">
                 <div className="lg:col-span-2 space-y-8">
                    <div>
                       <h3 className="text-2xl font-black mb-4 tracking-tighter">About this Lesson</h3>
                       <p className="text-white/60 leading-relaxed">
                         In this section, we dive deep into {activeLesson?.title}. Make sure to watch the entire video and review the attached resources for a full understanding of the topic.
                       </p>
                    </div>
                 </div>

                 <div className="space-y-8">
                    <div>
                       <h4 className="text-[10px] font-black uppercase tracking-widest text-primary mb-6">Course Resources</h4>
                       <div className="space-y-3">
                          {activeLesson?.resources?.map((res: LegacyResourceItem, idx: number) => (
                            <a 
                              key={idx} 
                              href={res.url} 
                              target="_blank" 
                              className="block glass-card p-4 hover:border-primary/40 transition-all flex items-center justify-between group"
                            >
                               <div className="flex items-center gap-3">
                                  <FileText size={18} className="text-white/20 group-hover:text-primary transition-colors" />
                                  <span className="text-xs font-bold truncate max-w-[150px]">{res.name}</span>
                               </div>
                               <ArrowRight size={14} className="text-white/10 group-hover:translate-x-1 transition-transform" />
                            </a>
                          ))}
                          {(!activeLesson?.resources || activeLesson.resources.length === 0) && (
                            <p className="text-xs text-white/20 italic">No additional resources for this lesson.</p>
                          )}
                       </div>
                    </div>
                 </div>
              </div>
           </div>
        </div>

        {/* Footer Navigation */}
        <footer className="px-8 py-6 bg-bg-secondary/50 backdrop-blur-xl border-t border-white/5 flex items-center justify-between sticky bottom-0">
           <button className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-white/40 hover:text-white transition-colors group">
              <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" /> Previous
           </button>
           <button className="flex items-center gap-2 bg-primary px-8 py-3 rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-primary-hover transition-all group shadow-[0_0_20px_rgba(59,130,246,0.3)] hover:scale-105 active:scale-[0.98]">
              Next Lesson <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
           </button>
        </footer>
      </main>
    </div>
  );
};

export default CoursePlayer;

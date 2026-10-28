import { useState } from 'react';
import { 
  Video, FileText, Save, ArrowLeft, 
  Trash2, GripVertical, PlusCircle, CheckCircle, Youtube
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { legacyApi } from '../../services/legacyApi';
import type { LegacyCourse, LegacyLesson, LegacyModule } from '../../services/apiTypes';
import { useToast } from '../../components/ToastProvider';
import { getErrorMessage } from '../../utils/errors';

const CourseBuilder = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [activeStep, setActiveStep] = useState(1);
  const [courseData, setCourseData] = useState<LegacyCourse>({
    title: '',
    description: '',
    category: 'Programming',
    difficulty: 'Beginner',
    modules: []
  });

  const addModule = () => {
    const newModule: LegacyModule = {
      title: `Module ${courseData.modules.length + 1}`,
      lessons: []
    };
    setCourseData({ ...courseData, modules: [...courseData.modules, newModule] });
  };

  const addLesson = (moduleIdx: number, type: 'video' | 'text' | 'pdf') => {
    const updatedModules = [...courseData.modules];
    const newLesson: LegacyLesson = {
      id: `lesson-${moduleIdx}-${updatedModules[moduleIdx].lessons.length}`,
      title: `New Lesson`,
      type,
      youtube_url: '',
      content: ''
    };
    updatedModules[moduleIdx].lessons.push(newLesson);
    setCourseData({ ...courseData, modules: updatedModules });
  };

  const saveCourse = async () => {
    try {
      await legacyApi.createCourse(courseData);
      toast.success('Course published successfully.');
      navigate('/dashboard');
    } catch (err) {
      console.error("Failed to save course", err);
      toast.error(getErrorMessage(err, 'Failed to save course.'));
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-10">
        <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-white/40 hover:text-white transition-colors">
          <ArrowLeft size={20} /> <span className="font-bold">Back to Courses</span>
        </button>
        <div className="flex gap-4">
          <button className="btn-primary bg-bg-accent text-white border border-white/10 flex items-center gap-2 hover:bg-bg-accent/80">
            <Save size={18} /> Save Draft
          </button>
          <button onClick={saveCourse} className="btn-primary flex items-center gap-2 shadow-[0_0_30px_rgba(59,130,246,0.3)]">
            <CheckCircle size={18} /> Publish Course
          </button>
        </div>
      </div>

      <div className="flex gap-10">
        {/* Progress Sidebar */}
        <div className="w-64 shrink-0 space-y-6">
           <div className={`p-4 rounded-2xl border ${activeStep === 1 ? 'bg-primary/10 border-primary/30 text-primary' : 'border-white/5 text-white/40'}`}>
             <p className="text-[10px] font-black uppercase tracking-widest mb-1">Step 01</p>
             <h3 className="font-bold">Course Info</h3>
           </div>
           <div className={`p-4 rounded-2xl border ${activeStep === 2 ? 'bg-primary/10 border-primary/30 text-primary' : 'border-white/5 text-white/40'}`}>
             <p className="text-[10px] font-black uppercase tracking-widest mb-1">Step 02</p>
             <h3 className="font-bold">Curriculum</h3>
           </div>
        </div>

        {/* Builder Panel */}
        <div className="flex-1 space-y-8">
          {activeStep === 1 ? (
            <div className="glass-card space-y-8">
              <div className="space-y-4">
                <label className="block text-sm font-bold text-white/70 uppercase tracking-widest ml-1">Course Title</label>
                <input 
                  type="text" 
                  className="input-field w-full text-xl font-bold py-4" 
                  placeholder="Enter a descriptive title..."
                  value={courseData.title}
                  onChange={(e) => setCourseData({...courseData, title: e.target.value})}
                />
              </div>
              <div className="space-y-4">
                <label className="block text-sm font-bold text-white/70 uppercase tracking-widest ml-1">Description</label>
                <textarea 
                  className="input-field w-full h-40 resize-none leading-relaxed" 
                  placeholder="What will students learn in this course?"
                  value={courseData.description}
                  onChange={(e) => setCourseData({...courseData, description: e.target.value})}
                />
              </div>
              <div className="grid grid-cols-2 gap-8">
                <div className="space-y-4">
                  <label className="block text-sm font-bold text-white/70 uppercase tracking-widest ml-1">Category</label>
                  <select 
                    className="input-field w-full"
                    value={courseData.category}
                    onChange={(e) => setCourseData({...courseData, category: e.target.value})}
                  >
                    <option>Programming</option>
                    <option>Data Science</option>
                    <option>Business</option>
                    <option>Marketing</option>
                  </select>
                </div>
                <div className="space-y-4">
                  <label className="block text-sm font-bold text-white/70 uppercase tracking-widest ml-1">Difficulty</label>
                  <select 
                    className="input-field w-full"
                    value={courseData.difficulty}
                    onChange={(e) => setCourseData({...courseData, difficulty: e.target.value})}
                  >
                    <option>Beginner</option>
                    <option>Intermediate</option>
                    <option>Advanced</option>
                  </select>
                </div>
              </div>
              <button 
                onClick={() => setActiveStep(2)}
                className="btn-primary w-full py-4 text-lg mt-6"
              >
                Go to Curriculum
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              {courseData.modules.map((module, mIdx) => (
                <div key={mIdx} className="glass-card group border-l-4 border-l-primary/30">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <GripVertical className="text-white/20 cursor-grab" />
                      <input 
                        type="text" 
                        className="bg-transparent border-none text-xl font-bold text-white focus:outline-none focus:ring-0" 
                        value={module.title}
                        onChange={(e) => {
                          const updated = [...courseData.modules];
                          updated[mIdx].title = e.target.value;
                          setCourseData({...courseData, modules: updated});
                        }}
                      />
                    </div>
                    <button className="text-red-500/50 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Trash2 size={20} />
                    </button>
                  </div>

                  <div className="space-y-4 mb-8">
                    {module.lessons.map((lesson, lIdx) => (
                      <div key={lIdx} className="bg-bg-accent/40 rounded-xl p-6 flex items-center justify-between group/lesson border border-white/5 hover:border-white/10 transition-all">
                        <div className="flex items-center gap-4 flex-1">
                          {lesson.type === 'video' ? <Youtube size={20} className="text-red-500" /> : <FileText size={20} className="text-primary" />}
                          <input 
                            type="text" 
                            className="bg-transparent border-none text-white font-semibold focus:outline-none focus:ring-0 flex-1" 
                            value={lesson.title}
                            onChange={(e) => {
                              const updated = [...courseData.modules];
                              updated[mIdx].lessons[lIdx].title = e.target.value;
                              setCourseData({...courseData, modules: updated});
                            }}
                          />
                        </div>
                        {lesson.type === 'video' && (
                          <input 
                            type="text" 
                            className="bg-bg-dark/50 border border-white/10 rounded-lg px-3 py-1.5 text-xs w-64 mr-4 text-white/60 focus:border-primary/50" 
                            placeholder="Paste YouTube URL..."
                            value={lesson.youtube_url}
                            onChange={(e) => {
                              const updated = [...courseData.modules];
                              updated[mIdx].lessons[lIdx].youtube_url = e.target.value;
                              setCourseData({...courseData, modules: updated});
                            }}
                          />
                        )}
                        <button className="text-white/20 hover:text-white transition-colors">
                          <Trash2 size={16} />
                        </button>
                      </div>
                    ))}
                  </div>

                  <div className="flex gap-4">
                    <button onClick={() => addLesson(mIdx, 'video')} className="flex items-center gap-2 text-xs font-bold text-white/40 hover:text-primary transition-colors bg-white/5 py-2 px-4 rounded-lg">
                      <Video size={14} /> Add Video
                    </button>
                    <button onClick={() => addLesson(mIdx, 'text')} className="flex items-center gap-2 text-xs font-bold text-white/40 hover:text-primary transition-colors bg-white/5 py-2 px-4 rounded-lg">
                      <FileText size={14} /> Add Reading
                    </button>
                  </div>
                </div>
              ))}

              <button 
                onClick={addModule}
                className="w-full border-2 border-dashed border-white/10 rounded-2xl py-10 flex flex-col items-center gap-3 text-white/40 hover:text-primary hover:border-primary/30 transition-all group"
              >
                <PlusCircle size={32} className="group-hover:scale-110 transition-transform" />
                <span className="font-bold tracking-widest text-sm uppercase">Add New Module</span>
              </button>
              
              <div className="flex gap-6 mt-10 pt-10 border-t border-white/5">
                 <button onClick={() => setActiveStep(1)} className="btn-primary bg-bg-accent hover:bg-bg-accent/80 flex-1">Back to Info</button>
                 <button onClick={saveCourse} className="btn-primary flex-1 shadow-[0_0_30px_rgba(59,130,246,0.3)]">Publish Course</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CourseBuilder;

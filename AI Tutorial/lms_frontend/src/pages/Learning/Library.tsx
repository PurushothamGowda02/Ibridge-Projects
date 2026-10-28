import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Star, Play, Sparkles, ArrowRight, WandSparkles } from 'lucide-react';

const seedCourses = [
  { id: 'c1', title: 'Python Programming', category: 'Programming', difficulty: 'Beginner', description: 'Learn core Python syntax, OOP, and real coding practice.' },
  { id: 'c2', title: 'Data Structures & Algorithms', category: 'Programming', difficulty: 'Intermediate', description: 'Master DSA for interviews with problem-solving patterns.' },
  { id: 'c3', title: 'Machine Learning Foundations', category: 'Data Science', difficulty: 'Intermediate', description: 'Build strong intuition for ML models and evaluation.' },
  { id: 'c4', title: 'Linear Algebra for AI', category: 'Mathematics', difficulty: 'Intermediate', description: 'Vectors, matrices, and transformations for modern AI.' },
  { id: 'c5', title: 'Digital Marketing', category: 'Business', difficulty: 'Beginner', description: 'SEO, ads, analytics, and campaign planning with projects.' },
  { id: 'c6', title: 'Aptitude & Reasoning', category: 'Interview Prep', difficulty: 'Beginner', description: 'Quant + logical reasoning for placement preparation.' },
];

const Library = () => {
  const [activeCategory, setActiveCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const categories = ['All', 'Programming', 'Data Science', 'Mathematics', 'Business', 'Soft Skills', 'UPSC', 'Interview Prep'];

  const filteredCourses = useMemo(() => {
    return seedCourses.filter((course) => {
      const categoryOk = activeCategory === 'All' || course.category === activeCategory;
      const query = searchQuery.trim().toLowerCase();
      const queryOk = !query || course.title.toLowerCase().includes(query) || course.description.toLowerCase().includes(query);
      return categoryOk && queryOk;
    });
  }, [activeCategory, searchQuery]);

  const startAiLearning = (subject: string, topic: string) => {
    navigate(`/ai-tutor?subject=${encodeURIComponent(subject)}&topic=${encodeURIComponent(topic)}`);
  };

  const launchCustomTopic = () => {
    const customTopic = searchQuery.trim() || 'Python OOP';
    const subject = activeCategory === 'All' ? 'Programming' : activeCategory;
    startAiLearning(subject, customTopic);
  };

  return (
    <div className="max-w-7xl mx-auto pb-20">
      <div className="mb-8 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h2 className="text-4xl font-black tracking-tight mb-2">Course <span className="text-primary italic">Library</span></h2>
          <p className="text-white/40 font-medium">Pick a subject and jump straight into personalized AI-generated learning.</p>
        </div>
        <button onClick={launchCustomTopic} className="btn-primary flex items-center gap-2">
          <WandSparkles size={16} /> Start AI Path
        </button>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 mb-12">
        <div className="relative flex-1 group">
          <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-white/20 group-focus-within:text-primary transition-colors" size={20} />
          <input
            type="text"
            placeholder="Search topic (example: Graph Theory, React Hooks, Calculus)..."
            className="input-field w-full pl-14 py-4 bg-bg-secondary/50 border-white/5 focus:border-primary/30"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="flex gap-2 bg-bg-secondary/30 p-1.5 rounded-2xl border border-white/5 overflow-x-auto no-scrollbar">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all whitespace-nowrap ${
                activeCategory === cat ? 'bg-primary text-white shadow-lg' : 'text-white/40 hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {filteredCourses.map((course) => (
          <div
            key={course.id}
            className="glass-card p-0 group overflow-hidden border-white/5 hover:border-primary/30 transition-all hover:-translate-y-1"
          >
            <div className="h-44 bg-bg-accent relative">
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-bg-accent to-bg-dark opacity-70">
                <Play size={40} className="text-primary/20" />
              </div>
              <div className="absolute inset-0 bg-gradient-to-t from-bg-dark to-transparent opacity-60"></div>
              <span className="absolute top-4 left-4 text-[10px] font-black uppercase tracking-widest text-primary bg-primary/10 px-3 py-1.5 rounded-full border border-primary/20 backdrop-blur-md">{course.difficulty}</span>
            </div>

            <div className="p-6">
              <div className="flex justify-between items-start mb-3">
                <p className="text-[10px] font-black uppercase tracking-widest text-white/30">{course.category}</p>
                <div className="flex items-center gap-1">
                  <Star size={10} className="text-yellow-500 fill-yellow-500" />
                  <span className="text-[10px] font-black text-yellow-500">AI Curated</span>
                </div>
              </div>

              <h3 className="text-xl font-black mb-3 leading-tight group-hover:text-primary transition-colors line-clamp-2 h-14">{course.title}</h3>

              <p className="text-sm text-white/40 mb-8 line-clamp-2 leading-relaxed">{course.description}</p>

              <div className="flex items-center justify-between">
                <div className="text-[10px] font-bold uppercase tracking-widest text-white/40">Personalized videos + tests + coding</div>
                <button
                  onClick={() => startAiLearning(course.category, course.title)}
                  className="bg-primary hover:bg-primary-hover text-white p-2.5 rounded-xl transition-all hover:scale-110 active:scale-95 shadow-[0_0_20px_rgba(59,130,246,0.3)]"
                >
                  <ArrowRight size={20} />
                </button>
              </div>
            </div>
          </div>
        ))}

        {filteredCourses.length === 0 && (
          <div className="col-span-full py-20 text-center flex flex-col items-center gap-6">
            <Sparkles size={48} className="text-white/10" />
            <div>
              <h3 className="text-xl font-black mb-2">No topic matched</h3>
              <p className="text-white/30">Try a different keyword, or click Start AI Path to generate a custom course.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Library;

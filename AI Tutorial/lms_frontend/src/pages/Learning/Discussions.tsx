const Discussions = () => {
  return (
    <div className="max-w-6xl mx-auto pb-20 space-y-6">
      <div>
        <h2 className="text-4xl font-extrabold tracking-tight">
          Course <span className="text-primary italic">Discussions</span>
        </h2>
        <p className="text-white/40 font-medium">
          Ask doubts, discuss solutions, and collaborate with peers and instructors.
        </p>
      </div>

      <section className="glass-card space-y-3">
        <h3 className="text-xl font-black">Purpose</h3>
        <p className="text-white/70 text-sm">
          This section is meant for Q&A, topic-wise threads, module help, and community interaction.
        </p>
      </section>

      <section className="glass-card">
        <p className="text-white/50 text-sm">
          Discussion features are now enabled as a page. Next step can be adding real threads/comments backed by API.
        </p>
      </section>
    </div>
  );
};

export default Discussions;


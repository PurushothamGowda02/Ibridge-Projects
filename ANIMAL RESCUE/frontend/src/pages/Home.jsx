import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, ShieldCheck, HeartPulse, Users } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="container">
            {/* Hero Section */}
            <section style={{ display: 'flex', alignItems: 'center', minHeight: '80vh', gap: '50px' }}>
                <div style={{ flex: 1 }}>
                    <motion.h1 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                        style={{ fontSize: '4.5rem', lineHeight: 1, marginBottom: '24px' }}
                    >
                        Find Your New <span style={{ color: 'var(--secondary-color)' }}>Best Friend</span>
                    </motion.h1>
                    <motion.p 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        style={{ fontSize: '1.2rem', color: 'var(--muted-text)', marginBottom: '32px' }}
                    >
                        Every year, thousands of animals are looking for a forever home. 
                        Our mission is to connect these loving souls with compassionate humans. 
                        Adopt, don't shop!
                    </motion.p>
                    <motion.div 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.4 }}
                        style={{ display: 'flex', gap: '16px' }}
                    >
                        <Link to="/adopt" className="btn btn-primary" style={{ padding: '16px 32px' }}>
                             Adopt Now <ArrowRight size={20} />
                        </Link>
                        <Link to="/report" className="btn glass-morphism" style={{ padding: '16px 32px' }}>
                            Report a Stray
                        </Link>
                    </motion.div>
                </div>
                <div style={{ flex: 1 }}>
                    <motion.div 
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.8 }}
                        className="glass-morphism"
                        style={{ padding: '10px', borderRadius: '24px' }}
                    >
                        <img 
                            src="/hero.png" 
                            alt="Hero" 
                            style={{ width: '100%', borderRadius: '20px', display: 'block' }} 
                        />
                    </motion.div>
                </div>
            </section>

            {/* Features Section */}
            <section style={{ padding: '100px 0', textAlign: 'center' }}>
                <h2 style={{ fontSize: '3rem', marginBottom: '60px' }}>How We Help</h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '30px' }}>
                    <div className="glass-morphism" style={{ padding: '40px' }}>
                        <ShieldCheck size={48} color="var(--primary-color)" style={{ marginBottom: '20px' }} />
                        <h3>Rescue & Protect</h3>
                        <p style={{ color: 'var(--muted-text)', marginTop: '10px' }}>We take in abandoned animals and provide them with a safe haven.</p>
                    </div>
                    <div className="glass-morphism" style={{ padding: '40px' }}>
                        <HeartPulse size={48} color="var(--secondary-color)" style={{ marginBottom: '20px' }} />
                        <h3>Medical Care</h3>
                        <p style={{ color: 'var(--muted-text)', marginTop: '10px' }}>All our rescues receive full vet checkups and vaccinations.</p>
                    </div>
                    <div className="glass-morphism" style={{ padding: '40px' }}>
                        <Users size={48} color="var(--accent-color)" style={{ marginBottom: '20px' }} />
                        <h3>Happy Adoptions</h3>
                        <p style={{ color: 'var(--muted-text)', marginTop: '10px' }}>We match pets with the perfect families for lifelong happiness.</p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;

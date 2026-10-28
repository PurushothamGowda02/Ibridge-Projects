import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Gift, Heart, Coffee, ShieldCheck, CheckCircle, Loader2 } from 'lucide-react';

const Donate = () => {
    const [selectedTier, setSelectedTier] = useState(null);
    const [loading, setLoading] = useState(false);
    const [donated, setDonated] = useState(false);
    const [donationAmount, setDonationAmount] = useState(null);

    const tiers = [
        { label: 'Starter', amount: '$10', value: 10, desc: 'Provides food for one pet for a week.', icon: <Coffee size={40} color="var(--primary-color)" /> },
        { label: 'Advocate', amount: '$50', value: 50, desc: 'Covers a full medical checkup and vaccination.', icon: <Heart size={40} color="var(--secondary-color)" /> },
        { label: 'Guardian', amount: '$150', value: 150, desc: 'Full care for a rescued animal until adoption.', icon: <ShieldCheck size={40} color="var(--accent-color)" /> }
    ];

    const handleDonate = async (tier) => {
        setSelectedTier(tier.value);
        setLoading(true);
        
        // Simulate payment processing
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        setLoading(false);
        setDonated(true);
        setDonationAmount(tier.value);
        
        // Reset after 5 seconds
        setTimeout(() => {
            setDonated(false);
            setSelectedTier(null);
            setDonationAmount(null);
        }, 5000);
    };

    return (
        <div className="container" style={{ padding: '40px 20px', textAlign: 'center' }}>
            <h1 style={{ fontSize: '3.5rem', marginBottom: '20px' }}>Support Our <span style={{ color: 'var(--secondary-color)' }}>Mission</span></h1>
            <p style={{ color: 'var(--muted-text)', fontSize: '1.2rem', maxWidth: '700px', margin: '0 auto 60px' }}>
                Your contributions go directly towards food, medical supplies, and shelter for animals in need. 
                Every bit helps us save another life.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '30px', marginBottom: '80px' }}>
                {tiers.map((tier, i) => (
                    <motion.div 
                        key={i}
                        whileHover={{ scale: 1.05 }}
                        animate={selectedTier === tier.value ? { scale: 1.1, boxShadow: '0 0 30px rgba(255, 107, 107, 0.5)' } : {}}
                        className="glass-morphism" 
                        style={{ 
                            padding: '50px 30px',
                            cursor: 'pointer',
                            border: selectedTier === tier.value ? '2px solid var(--secondary-color)' : '1px solid rgba(255,255,255,0.1)',
                            transition: 'all 0.3s ease'
                        }}
                    >
                        <div style={{ marginBottom: '24px' }}>{tier.icon}</div>
                        <h3 style={{ fontSize: '1.2rem', marginBottom: '10px', color: 'var(--muted-text)' }}>{tier.label}</h3>
                        <h2 style={{ fontSize: '3rem', marginBottom: '20px' }}>{tier.amount}</h2>
                        <p style={{ color: 'var(--muted-text)', marginBottom: '32px' }}>{tier.desc}</p>
                        <button 
                            className="btn btn-primary" 
                            style={{ width: '100%', justifyContent: 'center' }}
                            onClick={() => handleDonate(tier)}
                            disabled={loading && selectedTier === tier.value}
                        >
                            {loading && selectedTier === tier.value ? (
                                <><Loader2 className="animate-spin" /> Processing...</>
                            ) : (
                                'Donate Now'
                            )}
                        </button>
                    </motion.div>
                ))}
            </div>

            {/* Success Modal */}
            <AnimatePresence>
                {donated && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.5 }}
                        style={{
                            position: 'fixed',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            zIndex: 1000,
                            width: '90%',
                            maxWidth: '500px'
                        }}
                    >
                        <motion.div
                            className="glass-morphism"
                            style={{
                                padding: '60px 40px',
                                textAlign: 'center',
                                borderRadius: '32px',
                                boxShadow: '0 0 50px rgba(255, 107, 107, 0.3)'
                            }}
                            animate={{ y: [0, -10, 0] }}
                            transition={{ duration: 0.6, repeat: Infinity }}
                        >
                            <motion.div
                                animate={{ scale: [1, 1.2, 1] }}
                                transition={{ duration: 0.6 }}
                                style={{ marginBottom: '24px' }}
                            >
                                <CheckCircle size={80} color="var(--secondary-color)" />
                            </motion.div>
                            <h1 style={{ fontSize: '2.5rem', marginBottom: '16px', color: 'var(--secondary-color)' }}>
                                Thank You! 🎉
                            </h1>
                            <p style={{ fontSize: '1.3rem', marginBottom: '12px', fontWeight: '600' }}>
                                You've donated ${donationAmount}
                            </p>
                            <p style={{ color: 'var(--muted-text)', fontSize: '1rem', marginBottom: '24px' }}>
                                Your generous contribution will help us save more animal lives!
                            </p>
                            <motion.div
                                animate={{ width: ['0%', '100%'] }}
                                transition={{ duration: 5 }}
                                style={{
                                    height: '4px',
                                    background: 'linear-gradient(90deg, var(--secondary-color), var(--primary-color))',
                                    borderRadius: '2px'
                                }}
                            />
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Overlay */}
            <AnimatePresence>
                {donated && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        style={{
                            position: 'fixed',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            background: 'rgba(0, 0, 0, 0.5)',
                            zIndex: 999
                        }}
                    />
                )}
            </AnimatePresence>

            <div className="glass-morphism" style={{ padding: '60px', maxWidth: '800px', margin: '0 auto' }}>
                <Gift size={48} color="var(--accent-color)" style={{ marginBottom: '24px' }} />
                <h2 style={{ marginBottom: '16px' }}>Other Ways to Help</h2>
                <p style={{ color: 'var(--muted-text)', marginBottom: '32px' }}>
                    Don't have funds but want to help? We always need volunteers for walking dogs, 
                    cleaning shelters, and fostering pets. Contact us to learn more!
                </p>
                <button className="btn glass-morphism" style={{ padding: '16px 32px' }}>Contact Our Team</button>
            </div>
        </div>
    );
};

export default Donate;

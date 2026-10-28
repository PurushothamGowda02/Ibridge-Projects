import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Calendar, Heart, Loader2 } from 'lucide-react';
import { adoptionService } from '../services/api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const PetCard = ({ pet }) => {
    const [loading, setLoading] = useState(false);
    const [imageError, setImageError] = useState(false);
    const { addToast } = useToast();
    const { user } = useAuth();
    const navigate = useNavigate();

    const handleAdopt = async () => {
        if (!user) {
            addToast('Please login to adopt a pet', 'error');
            navigate('/login');
            return;
        }

        setLoading(true);
        try {
            await adoptionService.create({ 
                animal_id: pet.id, 
                message: `I would like to adopt ${pet.name}!` 
            });
            addToast(`Success! Your adoption request for ${pet.name} has been sent.`, 'success');
        } catch (error) {
            console.error('Adoption failed:', error);
            addToast(error.response?.data?.detail || 'Failed to send adoption request.', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleImageError = () => {
        setImageError(true);
        console.error('Failed to load image:', pet.image_url);
    };

    return (
        <motion.div 
            whileHover={{ y: -10 }}
            className="glass-morphism" 
            style={{ overflow: 'hidden' }}
        >
            <div style={{ height: '250px', overflow: 'hidden', background: 'rgba(255,255,255,0.05)' }}>
                {imageError ? (
                    <div style={{ 
                        width: '100%', 
                        height: '100%', 
                        display: 'flex', 
                        alignItems: 'center', 
                        justifyContent: 'center',
                        color: 'var(--muted-text)',
                        fontSize: '0.9rem'
                    }}>
                        Image not available
                    </div>
                ) : (
                    <img 
                        src={pet.image_url} 
                        alt={pet.name} 
                        onError={handleImageError}
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
                    />
                )}
            </div>
            <div style={{ padding: '24px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <h3 style={{ fontSize: '1.5rem' }}>{pet.name}</h3>
                    <span style={{ 
                        padding: '4px 12px', 
                        borderRadius: '20px', 
                        fontSize: '0.8rem', 
                        background: 'var(--primary-color)', 
                        color: 'white' 
                    }}>
                        {pet.species}
                    </span>
                </div>
                
                <div style={{ display: 'flex', gap: '16px', color: 'var(--muted-text)', fontSize: '0.9rem', marginBottom: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Calendar size={16} />
                        {pet.age}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Heart size={16} />
                        {pet.gender}
                    </div>
                </div>

                <p style={{ color: 'var(--muted-text)', fontSize: '0.95rem', marginBottom: '24px', height: '60px', overflow: 'hidden' }}>
                    {pet.description}
                </p>

                <button 
                    onClick={handleAdopt} 
                    disabled={loading}
                    className="btn btn-primary" 
                    style={{ width: '100%', justifyContent: 'center' }}
                >
                    {loading ? <Loader2 className="animate-spin" /> : `Adopt ${pet.name}`}
                </button>
            </div>
        </motion.div>
    );
};

export default PetCard;

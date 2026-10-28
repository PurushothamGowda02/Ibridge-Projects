import React, { useState } from 'react';
import { Camera, MapPin, Send, CheckCircle, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { reportService } from '../services/api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Report = () => {
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [images, setImages] = useState([]);
    const [formData, setFormData] = useState({
        animal_name: '',
        description: '',
        location: '',
        contact_info: ''
    });

    const { addToast } = useToast();
    const { user } = useAuth();
    const navigate = useNavigate();

    const handleImageChange = (e) => {
        const files = Array.from(e.target.files);
        if (files.length > 0) {
            setImages(files);
            addToast(`${files.length} image(s) selected`, 'success');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!user) {
            addToast('Please login to report a stray animal', 'error');
            navigate('/login');
            return;
        }

        setLoading(true);
        try {
            const submitData = new FormData();
            submitData.append('animal_name', formData.animal_name);
            submitData.append('description', formData.description);
            submitData.append('location', formData.location);
            submitData.append('contact_info', formData.contact_info);
            
            // Add images to form data
            images.forEach((image) => {
                submitData.append('images', image);
            });

            await reportService.create(submitData);
            addToast('Report submitted successfully! Thank you.', 'success');
            setSubmitted(true);
        } catch (error) {
            console.error('Report failed:', error);
            addToast('Failed to submit report. Please try again.', 'error');
        } finally {
            setLoading(false);
        }
    };

    if (submitted) {
        return (
            <div className="container" style={{ textAlign: 'center', padding: '100px 0' }}>
                <motion.div 
                    initial={{ scale: 0.5, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    style={{ background: 'var(--glass-bg)', padding: '60px', borderRadius: '32px', display: 'inline-block' }}
                >
                    <CheckCircle size={80} color="var(--primary-color)" style={{ marginBottom: '24px' }} />
                    <h1 style={{ fontSize: '3rem', marginBottom: '16px' }}>Report Received!</h1>
                    <p style={{ color: 'var(--muted-text)', fontSize: '1.2rem', maxWidth: '500px', margin: '0 auto' }}>
                        Thank you for your compassion. Our rescue team has been notified and will look into it as soon as possible.
                    </p>
                    <button 
                        className="btn btn-primary" 
                        style={{ marginTop: '40px' }}
                        onClick={() => {
                            setSubmitted(false);
                            setFormData({ animal_name: '', description: '', location: '', contact_info: '' });
                            setImages([]);
                        }}
                    >
                        Report Another Case
                    </button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="container" style={{ padding: '40px 20px' }}>
            <div style={{ display: 'flex', gap: '60px', alignItems: 'center' }}>
                <div style={{ flex: 1 }}>
                    <h1 style={{ fontSize: '3.5rem', marginBottom: '20px' }}>Report a <span style={{ color: 'var(--secondary-color)' }}>Strays</span></h1>
                    <p style={{ color: 'var(--muted-text)', fontSize: '1.1rem', marginBottom: '40px' }}>
                        Found an animal in distress? Use this form to alert our rescue team. 
                        Please provide as much detail as possible to help us locate them quickly.
                    </p>

                    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        <div className="glass-morphism" style={{ padding: '24px' }}>
                            <label style={{ display: 'block', marginBottom: '12px', fontWeight: '600' }}>Animal Name (Optional)</label>
                            <input 
                                type="text"
                                placeholder="Give the animal a name (e.g., Buddy, Luna)..."
                                value={formData.animal_name}
                                onChange={(e) => setFormData({...formData, animal_name: e.target.value})}
                                style={{ 
                                    width: '100%', 
                                    background: 'rgba(255,255,255,0.05)', 
                                    border: '1px solid var(--glass-border)', 
                                    borderRadius: '12px', 
                                    padding: '16px', 
                                    color: 'white',
                                    outline: 'none'
                                }}
                            />
                        </div>

                        <div className="glass-morphism" style={{ padding: '24px' }}>
                            <label style={{ display: 'block', marginBottom: '12px', fontWeight: '600' }}>Description</label>
                            <textarea 
                                required
                                placeholder="Describe the animal and its condition..."
                                value={formData.description}
                                onChange={(e) => setFormData({...formData, description: e.target.value})}
                                style={{ 
                                    width: '100%', 
                                    background: 'rgba(255,255,255,0.05)', 
                                    border: '1px solid var(--glass-border)', 
                                    borderRadius: '12px', 
                                    padding: '16px', 
                                    color: 'white', 
                                    minHeight: '120px',
                                    outline: 'none'
                                }}
                            />
                        </div>

                        <div className="glass-morphism" style={{ padding: '24px' }}>
                            <label style={{ display: 'block', marginBottom: '12px', fontWeight: '600' }}>Location</label>
                            <div style={{ display: 'flex', gap: '12px' }}>
                                <input 
                                    required
                                    type="text"
                                    placeholder="Enter nearby landmark or address..."
                                    value={formData.location}
                                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                                    style={{ 
                                        flex: 1, 
                                        background: 'rgba(255,255,255,0.05)', 
                                        border: '1px solid var(--glass-border)', 
                                        borderRadius: '12px', 
                                        padding: '16px', 
                                        color: 'white',
                                        outline: 'none'
                                    }}
                                />
                                <button type="button" className="btn glass-morphism" style={{ padding: '0 16px' }}>
                                    <MapPin size={20} />
                                </button>
                            </div>
                        </div>

                        <div className="glass-morphism" style={{ padding: '24px' }}>
                            <label style={{ display: 'block', marginBottom: '12px', fontWeight: '600' }}>Contact Info</label>
                            <input 
                                required
                                type="text"
                                placeholder="Phone number or Email..."
                                value={formData.contact_info}
                                onChange={(e) => setFormData({...formData, contact_info: e.target.value})}
                                style={{ 
                                    width: '100%', 
                                    background: 'rgba(255,255,255,0.05)', 
                                    border: '1px solid var(--glass-border)', 
                                    borderRadius: '12px', 
                                    padding: '16px', 
                                    color: 'white',
                                    outline: 'none'
                                }}
                            />
                        </div>

                        <button 
                            type="submit" 
                            disabled={loading}
                            className="btn btn-primary" 
                            style={{ padding: '20px', justifyContent: 'center', fontSize: '1.1rem' }}
                        >
                            {loading ? <Loader2 className="animate-spin" /> : <><Send size={20} /> Submit Report</>}
                        </button>
                    </form>
                </div>

                <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
                    <div className="glass-morphism" style={{ padding: '40px', textAlign: 'center', maxWidth: '400px' }}>
                        <Camera size={64} color="var(--muted-text)" style={{ marginBottom: '24px' }} />
                        <h3 style={{ marginBottom: '12px' }}>Upload Photos</h3>
                        <p style={{ color: 'var(--muted-text)', fontSize: '0.9rem', marginBottom: '24px' }}>
                            Photos significantly help our team identify and reach the animal faster.
                        </p>
                        <input 
                            type="file" 
                            id="image-input"
                            multiple 
                            accept="image/*"
                            onChange={handleImageChange}
                            style={{ display: 'none' }}
                        />
                        <button 
                            type="button"
                            className="btn glass-morphism" 
                            style={{ width: '100%', justifyContent: 'center' }}
                            onClick={() => document.getElementById('image-input').click()}
                        >
                            Choose Files
                        </button>
                        {images.length > 0 && (
                            <div style={{ marginTop: '16px', textAlign: 'left' }}>
                                <p style={{ color: 'var(--primary-color)', fontWeight: '600', marginBottom: '8px' }}>
                                    Selected: {images.length} image(s)
                                </p>
                                <ul style={{ fontSize: '0.85rem', color: 'var(--muted-text)' }}>
                                    {images.map((img, idx) => (
                                        <li key={idx} style={{ marginBottom: '4px' }}>
                                            {img.name}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Report;

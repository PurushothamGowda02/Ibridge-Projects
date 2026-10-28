import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, Heart, ClipboardList, Info, Loader2, Trash2, CheckCircle, Clock } from 'lucide-react';
import { reportService, petService, adoptionService } from '../services/api';
import { useToast } from '../context/ToastContext';

const AdminDashboard = () => {
    const [reports, setReports] = useState([]);
    const [animals, setAnimals] = useState([]);
    const [adoptions, setAdoptions] = useState([]);
    const [stats, setStats] = useState([
        { label: 'Total Animals', value: '0', icon: <Heart color="var(--secondary-color)" /> },
        { label: 'Rescue Reports', value: '0', icon: <ClipboardList color="var(--accent-color)" /> },
        { label: 'Adoption Requests', value: '0', icon: <Users color="var(--primary-color)" /> },
    ]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [deleting, setDeleting] = useState(null);
    const { addToast } = useToast();

    useEffect(() => {
        fetchData();
        // Auto-refresh every 2 seconds
        const interval = setInterval(fetchData, 2000);
        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        setRefreshing(true);
        try {
            const [reportRes, petRes, adoptionRes] = await Promise.all([
                reportService.getAll(),
                petService.getAll(),
                adoptionService.getAll()
            ]);
            
            setReports(reportRes.data);
            setAnimals(petRes.data);
            setAdoptions(adoptionRes.data);
            
            // Count animals with images
            const animalsWithImages = petRes.data.filter(animal => animal.image_url).length;
            
            setStats([
                { label: 'Total Animals', value: petRes.data.length.toString(), icon: <Heart color="var(--secondary-color)" /> },
                { label: 'Rescue Reports', value: reportRes.data.length.toString(), icon: <ClipboardList color="var(--accent-color)" /> },
                { label: 'Adoption Requests', value: adoptionRes.data.length.toString(), icon: <Users color="var(--primary-color)" /> },
            ]);
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const handleDeleteAnimal = async (animalId, animalName) => {
        if (!window.confirm(`Are you sure you want to delete ${animalName}?`)) {
            return;
        }

        setDeleting(animalId);
        try {
            await petService.delete(animalId);
            setAnimals(animals.filter(animal => animal.id !== animalId));
            setStats(stats.map(stat => 
                stat.label === 'Total Animals' 
                    ? { ...stat, value: (parseInt(stat.value) - 1).toString() }
                    : stat
            ));
            addToast(`${animalName} has been deleted successfully.`, 'success');
        } catch (error) {
            console.error('Delete failed:', error);
            addToast(error.response?.data?.detail || 'Failed to delete animal.', 'error');
        } finally {
            setDeleting(null);
        }
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '100px' }}>
                <Loader2 size={48} className="animate-spin" />
            </div>
        );
    }

    return (
        <div className="container" style={{ padding: '40px 20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
                <h1 style={{ fontSize: '3rem', margin: 0 }}>Admin <span style={{ color: 'var(--primary-color)' }}>Dashboard</span></h1>
                <button 
                    onClick={fetchData}
                    disabled={refreshing}
                    className="btn glass-morphism"
                    style={{ padding: '12px 24px', display: 'flex', alignItems: 'center', gap: '8px', opacity: refreshing ? 0.6 : 1 }}
                >
                    {refreshing ? <Loader2 size={18} className="animate-spin" /> : '🔄'} {refreshing ? 'Refreshing...' : 'Refresh'}
                </button>
            </div>

            {/* Stats Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '30px', marginBottom: '60px' }}>
                {stats.map((stat, i) => (
                    <motion.div 
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="glass-morphism" 
                        style={{ padding: '30px', display: 'flex', alignItems: 'center', gap: '20px' }}
                    >
                        <div style={{ background: 'rgba(255,255,255,0.05)', padding: '15px', borderRadius: '12px' }}>
                            {stat.icon}
                        </div>
                        <div>
                            <p style={{ color: 'var(--muted-text)', fontSize: '0.9rem' }}>{stat.label}</p>
                            <h2 style={{ fontSize: '2rem' }}>{stat.value}</h2>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Recent Activity */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '40px' }}>
                <div className="glass-morphism" style={{ padding: '30px' }}>
                    <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <ClipboardList size={22} /> Recent Rescue Reports
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {reports.length > 0 ? (
                            reports.slice(0, 5).map(report => (
                                <div key={report.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', borderRadius: '12px', background: 'rgba(255,255,255,0.03)' }}>
                                    <div>
                                        <p style={{ fontWeight: '600' }}>{report.description}</p>
                                        <p style={{ fontSize: '0.8rem', color: 'var(--muted-text)' }}>Location: {report.location}</p>
                                    </div>
                                    <span style={{ 
                                        padding: '4px 12px', 
                                        borderRadius: '20px', 
                                        fontSize: '0.8rem', 
                                        background: report.status === 'reported' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(16, 185, 129, 0.2)',
                                        color: report.status === 'reported' ? '#f59e0b' : '#10b981'
                                    }}>
                                        {report.status}
                                    </span>
                                </div>
                            ))
                        ) : (
                            <p style={{ color: 'var(--muted-text)', textAlign: 'center', padding: '20px' }}>No reports found.</p>
                        )}
                    </div>
                </div>

                <div className="glass-morphism" style={{ padding: '30px' }}>
                    <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Users size={22} /> Adoption Requests
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {adoptions.length > 0 ? (
                            adoptions.slice(0, 5).map(adoption => (
                                <div key={adoption.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', borderRadius: '12px', background: 'rgba(255,255,255,0.03)' }}>
                                    <div>
                                        <p style={{ fontWeight: '600' }}>Animal ID: {adoption.animal_id}</p>
                                        <p style={{ fontSize: '0.8rem', color: 'var(--muted-text)' }}>User ID: {adoption.user_id}</p>
                                    </div>
                                    <span style={{ 
                                        padding: '4px 12px', 
                                        borderRadius: '20px', 
                                        fontSize: '0.8rem', 
                                        background: adoption.status === 'pending' ? 'rgba(245, 158, 11, 0.2)' : adoption.status === 'approved' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                                        color: adoption.status === 'pending' ? '#f59e0b' : adoption.status === 'approved' ? '#10b981' : '#ef4444'
                                    }}>
                                        {adoption.status}
                                    </span>
                                </div>
                            ))
                        ) : (
                            <p style={{ color: 'var(--muted-text)', textAlign: 'center', padding: '20px' }}>No adoption requests.</p>
                        )}
                    </div>
                </div>

                <div className="glass-morphism" style={{ padding: '30px' }}>
                    <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Info size={22} /> System Status
                    </h3>
                    <div style={{ padding: '16px', borderRadius: '12px', border: '1px solid var(--primary-color)', background: 'rgba(99, 102, 241, 0.1)' }}>
                        <p style={{ fontSize: '0.9rem' }}>Backend API: Connected</p>
                        <p style={{ fontSize: '0.9rem', marginTop: '8px' }}>Database: SQLite (Active)</p>
                    </div>
                </div>
            </div>

            {/* Animals Management */}
            <div className="glass-morphism" style={{ padding: '30px', marginTop: '40px' }}>
                <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <Heart size={22} /> Manage Animals
                </h3>
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                                <th style={{ textAlign: 'left', padding: '12px', color: 'var(--muted-text)', fontWeight: '600' }}>Name</th>
                                <th style={{ textAlign: 'left', padding: '12px', color: 'var(--muted-text)', fontWeight: '600' }}>Species</th>
                                <th style={{ textAlign: 'left', padding: '12px', color: 'var(--muted-text)', fontWeight: '600' }}>Breed</th>
                                <th style={{ textAlign: 'left', padding: '12px', color: 'var(--muted-text)', fontWeight: '600' }}>Description</th>
                                <th style={{ textAlign: 'left', padding: '12px', color: 'var(--muted-text)', fontWeight: '600' }}>Status</th>
                                <th style={{ textAlign: 'center', padding: '12px', color: 'var(--muted-text)', fontWeight: '600' }}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {animals.length > 0 ? (
                                animals.map(animal => (
                                    <tr key={animal.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                        <td style={{ padding: '12px', fontWeight: '600' }}>{animal.name}</td>
                                        <td style={{ padding: '12px' }}>{animal.species}</td>
                                        <td style={{ padding: '12px' }}>{animal.breed}</td>
                                        <td style={{ padding: '12px', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={animal.description}>{animal.description}</td>
                                        <td style={{ padding: '12px' }}>
                                            <span style={{ 
                                                padding: '4px 12px', 
                                                borderRadius: '20px', 
                                                fontSize: '0.8rem', 
                                                background: animal.status === 'available' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(245, 158, 11, 0.2)',
                                                color: animal.status === 'available' ? '#10b981' : '#f59e0b'
                                            }}>
                                                {animal.status}
                                            </span>
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center' }}>
                                            <button
                                                onClick={() => handleDeleteAnimal(animal.id, animal.name)}
                                                disabled={deleting === animal.id}
                                                style={{
                                                    background: 'rgba(255, 107, 107, 0.2)',
                                                    border: '1px solid #ff6b6b',
                                                    color: '#ff6b6b',
                                                    padding: '8px 12px',
                                                    borderRadius: '8px',
                                                    cursor: deleting === animal.id ? 'not-allowed' : 'pointer',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '6px',
                                                    justifyContent: 'center',
                                                    opacity: deleting === animal.id ? 0.6 : 1,
                                                    transition: 'all 0.3s ease'
                                                }}
                                            >
                                                {deleting === animal.id ? (
                                                    <Loader2 size={16} className="animate-spin" />
                                                ) : (
                                                    <><Trash2 size={16} /> Delete</>
                                                )}
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ padding: '20px', textAlign: 'center', color: 'var(--muted-text)' }}>
                                        No animals found.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;

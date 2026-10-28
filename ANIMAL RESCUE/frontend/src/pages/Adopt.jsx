import React, { useState, useEffect } from 'react';
import PetCard from '../components/PetCard';
import { Search, Filter, Loader2 } from 'lucide-react';
import { petService } from '../services/api';

const Adopt = () => {
    const [pets, setPets] = useState([]);
    const [filter, setFilter] = useState('All');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchPets();
    }, [filter]);

    const fetchPets = async () => {
        setLoading(true);
        try {
            const params = filter !== 'All' ? { species: filter } : {};
            const response = await petService.getAll(params);
            setPets(response.data);
        } catch (error) {
            console.error('Failed to fetch pets:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ padding: '40px 20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '60px' }}>
                <div>
                    <h1 style={{ fontSize: '3.5rem', marginBottom: '10px' }}>Meet Our <span style={{ color: 'var(--primary-color)' }}>Residents</span></h1>
                    <p style={{ color: 'var(--muted-text)' }}>Find the perfect match for your home and lifestyle.</p>
                </div>
                
                <div style={{ display: 'flex', gap: '12px' }}>
                    <div className="glass-morphism" style={{ padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Filter size={18} color="var(--muted-text)" />
                        <select 
                            value={filter} 
                            onChange={(e) => setFilter(e.target.value)}
                            style={{ background: 'none', border: 'none', color: 'white', outline: 'none', cursor: 'pointer' }}
                        >
                            <option value="All">All Species</option>
                            <option value="Dog">Dogs</option>
                            <option value="Cat">Cats</option>
                        </select>
                    </div>
                </div>
            </div>

            {loading ? (
                <div style={{ display: 'flex', justifyContent: 'center', padding: '100px' }}>
                    <Loader2 size={48} className="animate-spin" />
                </div>
            ) : (
                <>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '40px' }}>
                        {pets.map(pet => (
                            <PetCard key={pet.id} pet={pet} />
                        ))}
                    </div>
                    
                    {pets.length === 0 && (
                        <div style={{ textAlign: 'center', padding: '100px 0' }}>
                            <p style={{ color: 'var(--muted-text)', fontSize: '1.2rem' }}>No pets found matching your criteria.</p>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default Adopt;

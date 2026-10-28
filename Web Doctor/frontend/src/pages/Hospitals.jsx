import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Building2, MapPin, Phone, Mail, Stethoscope, Clock, Award, Calendar, User } from 'lucide-react';

const Hospitals = () => {
  const [hospitals, setHospitals] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [hospitalAppointments, setHospitalAppointments] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedHospital, setSelectedHospital] = useState(null);

  useEffect(() => {
    const load = async () => {
      await Promise.all([fetchHospitals(), fetchDoctors()]);
      setLoading(false);
    };
    load();
  }, []);

  const fetchHospitals = async () => {
    try {
      const res = await axios.get('http://localhost:8000/hospitals');
      setHospitals(res.data);
    } catch (err) {
      console.error('Error fetching hospitals', err);
    }
  };

  const fetchDoctors = async () => {
    try {
      const res = await axios.get('http://localhost:8000/doctors');
      setDoctors(res.data);
    } catch (err) {
      console.error('Error fetching doctors', err);
    }
  };

  const getDoctorsByHospital = (hospitalId) => {
    return doctors.filter(doctor => doctor.hospital?.id === hospitalId);
  };

  const fetchHospitalAppointments = async (hospitalId) => {
    try {
      const res = await axios.get(`http://localhost:8000/hospitals/${hospitalId}/appointments`);
      setHospitalAppointments(prev => ({
        ...prev,
        [hospitalId]: res.data
      }));
    } catch (err) {
      console.error('Error fetching hospital appointments', err);
    }
  };

  const handleHospitalClick = async (hospital) => {
    const isSelected = selectedHospital?.id === hospital.id;
    setSelectedHospital(isSelected ? null : hospital);
    
    if (!isSelected && !hospitalAppointments[hospital.id]) {
      await fetchHospitalAppointments(hospital.id);
    }
  };

  if (loading) {
    return (
      <section className="section">
        <div className="container" style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="spinner" style={{ margin: '0 auto' }} />
          <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Loading hospitals...</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section">
      <div className="container">
        <div style={{ marginBottom: '2rem', textAlign: 'center' }}>
          <h1 style={{ fontSize: '2.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
            <Building2 size={32} color="var(--brand)" /> Our Partner Hospitals
          </h1>
          <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem', fontSize: '1.1rem' }}>
            Trusted healthcare facilities with experienced medical professionals
          </p>
        </div>

        {hospitals.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <Building2 size={48} color="var(--text-muted)" style={{ margin: '0 auto' }} />
            <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>No hospitals available at the moment.</p>
          </div>
        ) : (
          <div className="grid" style={{ gap: '1.5rem' }}>
            {hospitals.map((hospital) => {
              const hospitalDoctors = getDoctorsByHospital(hospital.id);
              const isSelected = selectedHospital?.id === hospital.id;

              return (
                <article 
                  key={hospital.id} 
                  className="card" 
                  style={{ 
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    border: isSelected ? '2px solid var(--brand)' : '1px solid var(--border)'
                  }}
                  onClick={() => handleHospitalClick(hospital)}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', gap: '1rem' }}>
                    <div style={{ flex: 1 }}>
                      <h2 style={{ fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Building2 size={24} color="var(--brand)" />
                        {hospital.name}
                      </h2>
                      
                      <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <p style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
                          <MapPin size={16} color="var(--brand)" />
                          <strong>Address:</strong> {hospital.address}, {hospital.city}
                        </p>
                        
                        <p style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
                          <Phone size={16} color="var(--brand)" />
                          <strong>Phone:</strong> {hospital.phone}
                        </p>
                        
                        {hospital.email && (
                          <p style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
                            <Mail size={16} color="var(--brand)" />
                            <strong>Email:</strong> {hospital.email}
                          </p>
                        )}
                      </div>

                      {hospital.description && (
                        <p style={{ 
                          marginTop: '1rem', 
                          color: 'var(--text-muted)', 
                          lineHeight: '1.6',
                          padding: '0.75rem',
                          background: 'var(--surface-muted)',
                          borderRadius: '0.5rem'
                        }}>
                          {hospital.description}
                        </p>
                      )}
                    </div>

                    <div style={{ 
                      display: 'flex', 
                      flexDirection: 'column', 
                      alignItems: 'center',
                      padding: '0.75rem',
                      background: 'var(--surface-muted)',
                      borderRadius: '0.5rem',
                      minWidth: '100px'
                    }}>
                      <Stethoscope size={24} color="var(--brand)" />
                      <p style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--brand)', marginTop: '0.25rem' }}>
                        {hospitalDoctors.length}
                      </p>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                        {hospitalDoctors.length === 1 ? 'Doctor' : 'Doctors'}
                      </p>
                    </div>
                  </div>

                  {isSelected && hospitalDoctors.length > 0 && (
                    <div style={{ 
                      marginTop: '1.5rem', 
                      paddingTop: '1.5rem', 
                      borderTop: '1px solid var(--border)' 
                    }}>
                      <h3 style={{ 
                        fontSize: '1.2rem', 
                        marginBottom: '1rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem'
                      }}>
                        <Stethoscope size={20} color="var(--brand)" />
                        Medical Staff
                      </h3>
                      
                      <div className="grid grid-2" style={{ gap: '1rem' }}>
                        {hospitalDoctors.map((doctor) => (
                          <div 
                            key={doctor.id} 
                            className="card" 
                            style={{ 
                              boxShadow: 'none',
                              background: 'var(--surface-muted)',
                              border: '1px solid var(--border)'
                            }}
                          >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                              <div>
                                <p style={{ fontWeight: 800, fontSize: '1.1rem' }}>
                                  {doctor.user?.full_name}
                                </p>
                                <p style={{ color: 'var(--brand)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
                                  {doctor.specialty}
                                </p>
                              </div>
                              <div style={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                gap: '0.25rem',
                                background: 'var(--warning)',
                                padding: '0.25rem 0.5rem',
                                borderRadius: '0.25rem'
                              }}>
                                <Award size={14} />
                                <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>
                                  {doctor.rating}/5
                                </span>
                              </div>
                            </div>
                            
                            <p style={{ 
                              color: 'var(--text-muted)', 
                              fontSize: '0.85rem', 
                              marginTop: '0.5rem',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '0.35rem'
                            }}>
                              <Clock size={14} />
                              {doctor.experience} years of experience
                            </p>
                            
                            <p style={{ 
                              color: 'var(--text-muted)', 
                              fontSize: '0.85rem', 
                              marginTop: '0.5rem',
                              lineHeight: '1.5'
                            }}>
                              {doctor.bio}
                            </p>

                            {doctor.user?.phone_number && (
                              <p style={{ 
                                color: 'var(--text-muted)', 
                                fontSize: '0.85rem', 
                                marginTop: '0.5rem',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.35rem'
                              }}>
                                <Phone size={14} />
                                {doctor.user.phone_number}
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {isSelected && hospitalDoctors.length === 0 && (
                    <div style={{ 
                      marginTop: '1.5rem', 
                      paddingTop: '1.5rem', 
                      borderTop: '1px solid var(--border)',
                      textAlign: 'center',
                      color: 'var(--text-muted)'
                    }}>
                      <p>No doctors currently assigned to this hospital.</p>
                    </div>
                  )}

                  {isSelected && hospitalAppointments[hospital.id] && hospitalAppointments[hospital.id].length > 0 && (
                    <div style={{ 
                      marginTop: '1.5rem', 
                      paddingTop: '1.5rem', 
                      borderTop: '1px solid var(--border)' 
                    }}>
                      <h3 style={{ 
                        fontSize: '1.2rem', 
                        marginBottom: '1rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem'
                      }}>
                        <Calendar size={20} color="var(--brand)" />
                        Recent Appointments ({hospitalAppointments[hospital.id].length})
                      </h3>
                      
                      <div className="grid" style={{ gap: '0.75rem' }}>
                        {hospitalAppointments[hospital.id].slice(0, 5).map((appointment) => (
                          <div 
                            key={appointment.id} 
                            className="card" 
                            style={{ 
                              boxShadow: 'none',
                              background: 'var(--surface-muted)',
                              border: '1px solid var(--border)',
                              padding: '0.75rem'
                            }}
                          >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                              <div>
                                <p style={{ fontWeight: 700, fontSize: '0.95rem', margin: 0 }}>
                                  <User size={14} style={{ transform: 'translateY(2px)' }} /> Patient ID: {appointment.patient_id}
                                </p>
                                <p style={{ color: 'var(--brand)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
                                  Dr. {appointment.doctor?.user?.full_name}
                                </p>
                              </div>
                              <span className={`badge ${appointment.status === 'scheduled' ? 'badge-warning' : 'badge-success'}`}>
                                {appointment.status}
                              </span>
                            </div>
                            
                            <p style={{ 
                              color: 'var(--text-muted)', 
                              fontSize: '0.85rem',
                              margin: '0.25rem 0',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '0.35rem'
                            }}>
                              <Clock size={14} />
                              {new Date(appointment.appointment_date).toLocaleString('en-IN', {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                              })}
                            </p>

                            <p style={{ 
                              color: 'var(--text-muted)', 
                              fontSize: '0.85rem', 
                              marginTop: '0.5rem',
                              fontStyle: 'italic'
                            }}>
                              Symptoms: {appointment.symptoms}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <p style={{ 
                    marginTop: '1rem', 
                    fontSize: '0.85rem', 
                    color: 'var(--text-muted)',
                    textAlign: 'center',
                    fontStyle: 'italic'
                  }}>
                    {isSelected ? 'Click to collapse' : 'Click to view doctors'}
                  </p>
                </article>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
};

export default Hospitals;

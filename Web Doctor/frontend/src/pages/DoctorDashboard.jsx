import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Calendar, CheckCircle, ClipboardCheck, Clock, Users } from 'lucide-react';

const DoctorDashboard = ({ user }) => {
  const [appointments, setAppointments] = useState([]);
  const [pendingReviews, setPendingReviews] = useState([]);
  const [reviewForms, setReviewForms] = useState({});
  const [doctorProfile, setDoctorProfile] = useState(null);

  useEffect(() => {
    const load = async () => {
      await Promise.all([fetchDoctorProfile(), fetchAppointments(), fetchPendingReviews()]);
    };
    load();
  }, []);

  const authHeaders = () => {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  const fetchDoctorProfile = async () => {
    try {
      const res = await axios.get('http://localhost:8000/doctors', { headers: authHeaders() });
      const myProfile = res.data.find(d => d.user.id === user.id);
      setDoctorProfile(myProfile);
    } catch (err) {
      console.error('Error fetching doctor profile', err);
    }
  };

  const fetchAppointments = async () => {
    try {
      const res = await axios.get('http://localhost:8000/appointments', { headers: authHeaders() });
      setAppointments(res.data);
    } catch (err) {
      console.error('Error fetching appointments', err);
    }
  };

  const fetchPendingReviews = async () => {
    try {
      const res = await axios.get('http://localhost:8000/ai/reviews/pending', { headers: authHeaders() });
      setPendingReviews(res.data);
    } catch (err) {
      console.error('Error fetching pending reviews', err);
    }
  };

  const updateForm = (analysisId, key, value) => {
    setReviewForms((prev) => ({
      ...prev,
      [analysisId]: {
        verdict: 'approved',
        corrected_condition: '',
        corrected_severity: '',
        notes: '',
        ...(prev[analysisId] || {}),
        [key]: value,
      },
    }));
  };

  const submitReview = async (analysisId) => {
    const payload = reviewForms[analysisId] || {
      verdict: 'approved',
      corrected_condition: '',
      corrected_severity: '',
      notes: '',
    };

    try {
      await axios.post(`http://localhost:8000/ai/reviews/${analysisId}`, payload, { headers: authHeaders() });
      await fetchPendingReviews();
    } catch (err) {
      console.error('Error submitting review', err);
    }
  };

  const pendingAppointments = appointments.filter((a) => a.status === 'scheduled').length;
  const completedAppointments = appointments.filter((a) => a.status === 'completed').length;

  return (
    <section className="section">
      <div className="container">
        <div style={{ marginBottom: '1rem' }}>
          <h1 style={{ fontSize: '2rem' }}>Doctor Clinical Review Panel</h1>
          <p style={{ color: 'var(--text-muted)' }}>
            Welcome {user.full_name}. Review AI triage records for patient safety and quality control.
          </p>
          {doctorProfile?.hospital && (
            <p style={{ color: 'var(--brand)', marginTop: '0.3rem', fontWeight: 600 }}>
              🏥 {doctorProfile.hospital.name}, {doctorProfile.hospital.city} | 📞 {doctorProfile.hospital.phone}
            </p>
          )}
        </div>

        <div className="grid grid-3" style={{ marginBottom: '1rem' }}>
          <article className="metric">
            <p style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)' }}><Users size={14} /> Appointments</p>
            <p className="metric-value">{appointments.length}</p>
          </article>
          <article className="metric">
            <p style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)' }}><Clock size={14} /> Pending Visits</p>
            <p className="metric-value">{pendingAppointments}</p>
          </article>
          <article className="metric">
            <p style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)' }}><CheckCircle size={14} /> Completed</p>
            <p className="metric-value">{completedAppointments}</p>
          </article>
        </div>

        <div className="layout-2-1">
          <article className="card">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
              <Calendar size={18} color="var(--brand)" /> Upcoming Consultations
            </h3>
            {appointments.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', marginTop: '0.7rem' }}>No appointments scheduled.</p>
            ) : (
              <div className="grid" style={{ marginTop: '0.75rem' }}>
                {appointments.map((app) => (
                  <div key={app.id} className="card" style={{ boxShadow: 'none' }}>
                    <p style={{ fontWeight: 700 }}>Patient ID: {app.patient_id}</p>
                    <p style={{ color: 'var(--text-muted)' }}>{new Date(app.appointment_date).toLocaleDateString('en-US')}</p>
                    <p style={{ color: 'var(--text-muted)', marginTop: '0.25rem' }}>{app.symptoms}</p>
                    <span className={`badge ${app.status === 'scheduled' ? 'badge-warning' : 'badge-success'}`} style={{ marginTop: '0.4rem' }}>
                      {app.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </article>

          <article className="card">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
              <ClipboardCheck size={18} color="var(--brand)" /> Pending AI Review Queue
            </h3>
            {pendingReviews.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', marginTop: '0.7rem' }}>No pending triage records.</p>
            ) : (
              <div className="grid" style={{ marginTop: '0.75rem' }}>
                {pendingReviews.map((item) => {
                  const form = reviewForms[item.id] || {
                    verdict: 'approved',
                    corrected_condition: '',
                    corrected_severity: '',
                    notes: '',
                  };

                  return (
                    <div key={item.id} className="card" style={{ boxShadow: 'none' }}>
                      <p style={{ fontWeight: 700 }}>{item.predicted_condition}</p>
                      <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
                        Severity: {item.predicted_severity} | Lang: {item.input_language}
                      </p>
                      <p style={{ color: 'var(--text-muted)', marginTop: '0.25rem', fontSize: '0.9rem' }}>{item.raw_symptoms}</p>

                      <div className="input-group" style={{ marginTop: '0.6rem' }}>
                        <label>Verdict</label>
                        <select value={form.verdict} onChange={(e) => updateForm(item.id, 'verdict', e.target.value)}>
                          <option value="approved">Approved</option>
                          <option value="corrected">Corrected</option>
                          <option value="escalate">Escalate</option>
                        </select>
                      </div>

                      <div className="input-group">
                        <label>Corrected Condition (optional)</label>
                        <input
                          type="text"
                          value={form.corrected_condition}
                          onChange={(e) => updateForm(item.id, 'corrected_condition', e.target.value)}
                          placeholder="Enter corrected condition"
                        />
                      </div>

                      <div className="input-group">
                        <label>Corrected Severity (optional)</label>
                        <input
                          type="text"
                          value={form.corrected_severity}
                          onChange={(e) => updateForm(item.id, 'corrected_severity', e.target.value)}
                          placeholder="Low / Moderate / Emergency"
                        />
                      </div>

                      <div className="input-group">
                        <label>Clinician Notes</label>
                        <textarea
                          value={form.notes}
                          onChange={(e) => updateForm(item.id, 'notes', e.target.value)}
                          placeholder="Review reasoning and safety notes"
                        />
                      </div>

                      <button className="btn btn-primary" onClick={() => submitReview(item.id)}>
                        Submit Review
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </article>
        </div>
      </div>
    </section>
  );
};

export default DoctorDashboard;

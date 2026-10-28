import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  AlertTriangle,
  Calendar,
  CheckCircle,
  Clock,
  Globe2,
  Info,
  Search,
  Stethoscope,
  Brain,
  Activity,
  TrendingUp,
  Award,
  MapPin,
  Phone,
} from 'lucide-react';

const SEVERITY_META = {
  Emergency: { color: 'var(--danger)', width: '100%', badgeClass: 'badge-emergency' },
  High: { color: 'var(--danger)', width: '78%', badgeClass: 'badge-danger' },
  Moderate: { color: 'var(--warning)', width: '58%', badgeClass: 'badge-warning' },
  Low: { color: 'var(--success)', width: '30%', badgeClass: 'badge-success' },
};

const getMeta = (severity) => SEVERITY_META[severity] || SEVERITY_META.Low;

const PatientDashboard = ({ user }) => {
  const [symptoms, setSymptoms] = useState('');
  const [language, setLanguage] = useState('en');
  const [analysis, setAnalysis] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);
  const [auditHistory, setAuditHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const examples = {
    en: [
      'Fever with sore throat and body pain',
      'Chest tightness with shortness of breath',
      'Vomiting and loose motion since morning',
      'Itchy skin rash after new soap',
    ],
    hi: [
      'mujhe bukhar aur khansi hai',
      'सीने में दर्द और सांस लेने में दिक्कत',
      'pet dard, ulti aur dast ho rahe hain',
      'sar dard aur chakkar aa raha hai',
    ],
  };

  useEffect(() => {
    const load = async () => {
      await Promise.all([fetchDoctors(), fetchAppointments(), fetchModelInfo(), fetchMyAudits()]);
    };
    load();
  }, []);

  const authHeaders = () => {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  const fetchDoctors = async () => {
    try {
      const res = await axios.get('http://localhost:8000/doctors');
      setDoctors(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchAppointments = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;
      const res = await axios.get('http://localhost:8000/appointments', { headers: authHeaders() });
      setAppointments(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchModelInfo = async () => {
    try {
      const res = await axios.get('http://localhost:8000/ai/model-info');
      setModelInfo(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchMyAudits = async () => {
    try {
      const res = await axios.get('http://localhost:8000/ai/audits/me', { headers: authHeaders() });
      setAuditHistory(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!symptoms.trim()) return;

    setLoading(true);
    setError('');
    try {
      const res = await axios.post(
        'http://localhost:8000/ai/analyze',
        { symptoms, language },
        { headers: authHeaders() }
      );
      setAnalysis(res.data);
      await fetchMyAudits();
    } catch (err) {
      setError('Unable to analyze symptoms right now. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const bookAppointment = async (doctorId) => {
    try {
      await axios.post(
        'http://localhost:8000/appointments',
        {
          doctor_id: doctorId,
          appointment_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
          symptoms: symptoms || 'General health follow-up',
        },
        { headers: authHeaders() }
      );
      await fetchAppointments();
    } catch (err) {
      setError('Appointment booking failed. Please retry.');
      console.error(err);
    }
  };

  const meta = analysis ? getMeta(analysis.severity) : null;

  return (
    <section className="section">
      <div className="container">
        <div style={{ marginBottom: '1rem' }}>
          <h1 style={{ fontSize: '2rem' }}>Patient Care Dashboard</h1>
          <p style={{ color: 'var(--text-muted)' }}>
            Hello {user.full_name}. Get medical-first triage guidance in English or Hindi before spending on hospital visits.
          </p>
        </div>

        <div className="layout-2-1">
          <div className="grid" style={{ gap: '1rem' }}>
            <article className="card">
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <Search size={18} color="var(--brand)" /> Symptom Triage
              </h3>
              <p style={{ color: 'var(--text-muted)', marginTop: '0.35rem' }}>
                Write symptoms in plain text. The engine handles English, Hindi, and Hinglish patterns.
              </p>

              <div className="input-group" style={{ marginTop: '0.7rem' }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <Globe2 size={14} /> Input Language
                </label>
                <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                  <option value="en">English</option>
                  <option value="hi">Hindi / Hinglish</option>
                </select>
              </div>

              <div className="chip-row" style={{ marginTop: '0.4rem' }}>
                {examples[language].map((sample) => (
                  <button key={sample} type="button" className="chip" onClick={() => setSymptoms(sample)}>
                    {sample}
                  </button>
                ))}
              </div>

              <form onSubmit={handleAnalyze} style={{ marginTop: '0.9rem' }}>
                <div className="input-group">
                  <label>Symptoms</label>
                  <textarea
                    placeholder="Example: bukhar, khansi aur gale mein dard"
                    value={symptoms}
                    onChange={(e) => setSymptoms(e.target.value)}
                    required
                  />
                </div>

                <button type="submit" className="btn btn-primary" disabled={loading || !symptoms.trim()} style={{ width: '100%' }}>
                  {loading ? <span className="spinner" /> : <Search size={16} />} Analyze Symptoms
                </button>
              </form>

              {error && (
                <div className="warning-panel" style={{ marginTop: '0.75rem', display: 'flex', gap: '0.45rem' }}>
                  <AlertTriangle size={16} color="var(--danger)" />
                  <p style={{ color: 'var(--danger)', fontWeight: 700 }}>{error}</p>
                </div>
              )}

              {analysis && (
                <div className="card" style={{ marginTop: '1rem', background: 'var(--surface-muted)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.65rem' }}>
                    <h4 style={{ marginBottom: '0.35rem' }}>Triage Result</h4>
                    <span className={`badge ${meta.badgeClass}`}>{analysis.severity}</span>
                  </div>

                  <p><strong>Possible condition:</strong> {analysis.condition}</p>
                  <p><strong>Recommended specialist:</strong> {analysis.specialist}</p>
                  <p style={{ marginTop: '0.4rem', color: 'var(--text-muted)' }}>{analysis.recommendation}</p>

                  <div className="severity-bar">
                    <div className="severity-bar-fill" style={{ width: meta.width, background: meta.color }} />
                  </div>

                  <p style={{ marginTop: '0.4rem', fontSize: '0.86rem', color: 'var(--text-muted)' }}>
                    Model source: {analysis.model_source} | Language: {analysis.input_language}
                  </p>

                  <div className="grid grid-2" style={{ marginTop: '0.8rem' }}>
                    <div>
                      <h5 style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
                        <CheckCircle size={15} color="var(--success)" /> First-aid steps
                      </h5>
                      <ul style={{ paddingLeft: '1.1rem', marginTop: '0.35rem', color: 'var(--text-muted)' }}>
                        {analysis.first_aid.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
                        <AlertTriangle size={15} color="var(--danger)" /> Precautions
                      </h5>
                      <ul style={{ paddingLeft: '1.1rem', marginTop: '0.35rem', color: 'var(--text-muted)' }}>
                        {analysis.precaution.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </article>

            <article className="card">
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <Stethoscope size={18} color="var(--brand)" /> Available Doctors
              </h3>
              <div className="grid" style={{ marginTop: '0.75rem' }}>
                {doctors.length === 0 && <p style={{ color: 'var(--text-muted)' }}>No doctors currently listed.</p>}
                {doctors.map((doctor) => (
                  <div key={doctor.id} className="card" style={{ boxShadow: 'none' }}>
                    <p style={{ fontWeight: 800 }}>{doctor.user?.full_name}</p>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{doctor.specialty} - {doctor.experience} years</p>
                    {doctor.hospital && (
                      <p style={{ color: 'var(--brand)', fontSize: '0.88rem', marginTop: '0.25rem' }}>
                        📍 {doctor.hospital.name}, {doctor.hospital.city}
                      </p>
                    )}
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.15rem' }}>{doctor.bio}</p>
                    <button className="btn btn-outline" style={{ marginTop: '0.55rem' }} onClick={() => bookAppointment(doctor.id)}>
                      Book Consultation
                    </button>
                  </div>
                ))}
              </div>
            </article>
          </div>

          <aside className="grid" style={{ gap: '1rem', alignSelf: 'start' }}>
            <article className="model-panel">
              <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <Brain size={16} color="var(--brand)" /> Medical AI Model
              </h4>
              {modelInfo ? (
                <>
                  <p style={{ marginTop: '0.35rem' }}><strong>{modelInfo.name}</strong></p>
                  <p style={{ color: 'var(--text-muted)', marginTop: '0.2rem' }}>{modelInfo.type}</p>
                  <p style={{ color: 'var(--text-muted)', marginTop: '0.4rem', fontSize: '0.88rem' }}>{modelInfo.clinical_scope}</p>
                  <ul style={{ paddingLeft: '1rem', marginTop: '0.5rem', color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                    {modelInfo.datasets.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </>
              ) : (
                <p style={{ color: 'var(--text-muted)', marginTop: '0.4rem' }}>Loading model details...</p>
              )}
            </article>

            <article className="card">
              <h4 style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
                <Calendar size={16} color="var(--brand)" /> My Appointments
              </h4>
              {appointments.length === 0 ? (
                <p style={{ marginTop: '0.5rem', color: 'var(--text-muted)' }}>No appointments booked yet.</p>
              ) : (
                <div className="grid" style={{ marginTop: '0.55rem' }}>
                  {appointments.map((app) => (
                    <div key={app.id} className="card" style={{ boxShadow: 'none' }}>
                      <p style={{ fontWeight: 700 }}>{app.doctor?.user?.full_name || 'Assigned Doctor'}</p>
                      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                        <Clock size={13} style={{ transform: 'translateY(2px)' }} />{' '}
                        {new Date(app.appointment_date).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                        })}
                      </p>
                      <span className={`badge ${app.status === 'scheduled' ? 'badge-warning' : 'badge-success'}`} style={{ marginTop: '0.3rem' }}>
                        {app.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </article>

            <article className="card">
              <h4 style={{ marginBottom: '0.5rem' }}>My Triage Audit History</h4>
              {auditHistory.length === 0 ? (
                <p style={{ color: 'var(--text-muted)' }}>No triage records yet.</p>
              ) : (
                <div className="grid">
                  {auditHistory.slice(0, 6).map((record) => (
                    <div key={record.id} className="card" style={{ boxShadow: 'none' }}>
                      <p style={{ fontWeight: 700 }}>{record.predicted_condition}</p>
                      <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>{record.input_language} | {record.model_source}</p>
                      <span className={`badge ${record.review_status === 'reviewed' ? 'badge-success' : 'badge-warning'}`} style={{ marginTop: '0.35rem' }}>
                        {record.review_status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </article>

            <article className="warning-panel">
              <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--danger)' }}>
                <AlertTriangle size={16} /> Emergency Warning
              </h4>
              <p style={{ marginTop: '0.35rem', color: 'var(--danger)', fontWeight: 700 }}>
                For severe chest pain, breathing difficulty, stroke signs, uncontrolled bleeding, or unconsciousness, call your local emergency number now.
              </p>
            </article>

            <article className="card" style={{ background: 'var(--surface-muted)' }}>
              <p style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)' }}>
                <Info size={14} /> Guidance only, not a final diagnosis.
              </p>
            </article>
          </aside>
        </div>
      </div>
    </section>
  );
};

export default PatientDashboard;

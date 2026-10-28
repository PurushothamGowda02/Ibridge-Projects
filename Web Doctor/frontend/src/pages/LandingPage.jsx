import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ShieldCheck, Wallet, Activity, Brain, BookOpen, Stethoscope } from 'lucide-react';

const trustItems = [
  {
    icon: <Brain size={20} color="var(--brand)" />,
    title: 'Medical AI Triage',
    text: 'Domain-focused symptom triage logic designed for primary care and first-aid guidance.',
  },
  {
    icon: <BookOpen size={20} color="var(--brand)" />,
    title: 'Clinical Dataset Layer',
    text: 'Dataset profiles map symptoms to conditions, specialty, severity, and safe next steps.',
  },
  {
    icon: <ShieldCheck size={20} color="var(--brand)" />,
    title: 'Safety First Rules',
    text: 'Emergency red flags trigger high-priority alerts and clear instructions to seek urgent care.',
  },
];

const LandingPage = () => {
  return (
    <div className="animate-fade-in">
      <section className="section">
        <div className="container">
          <h1 className="hero-title">
            Healthcare help for people who need <mark>affordable answers first</mark>
          </h1>
          <p className="hero-sub">
            Web Doctor gives quick medical triage guidance for common illness symptoms, so people can take safer first steps before spending on hospital visits.
          </p>

          <div style={{ marginTop: '1.4rem', display: 'flex', gap: '0.7rem', flexWrap: 'wrap' }}>
            <Link to="/register" className="btn btn-primary">
              Start Free Check <ArrowRight size={16} />
            </Link>
            <Link to="/login" className="btn btn-outline">Sign In</Link>
          </div>

          <div className="grid grid-3" style={{ marginTop: '1.5rem' }}>
            <div className="metric">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <Wallet size={16} color="var(--brand)" />
                <span style={{ color: 'var(--text-muted)', fontWeight: 700 }}>Affordable Triage</span>
              </div>
              <p className="metric-value">Low-cost first step</p>
            </div>
            <div className="metric">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <Activity size={16} color="var(--brand)" />
                <span style={{ color: 'var(--text-muted)', fontWeight: 700 }}>Rapid Guidance</span>
              </div>
              <p className="metric-value">Under 1 minute</p>
            </div>
            <div className="metric">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <Stethoscope size={16} color="var(--brand)" />
                <span style={{ color: 'var(--text-muted)', fontWeight: 700 }}>Doctor Referral</span>
              </div>
              <p className="metric-value">Right specialist path</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container grid grid-3">
          {trustItems.map((item) => (
            <article key={item.title} className="card">
              {item.icon}
              <h3 style={{ marginTop: '0.7rem' }}>{item.title}</h3>
              <p style={{ color: 'var(--text-muted)', marginTop: '0.45rem' }}>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container card" style={{ background: 'var(--surface-muted)' }}>
          <h2 style={{ fontSize: '1.6rem' }}>How this helps a common family</h2>
          <div className="grid grid-3" style={{ marginTop: '0.9rem' }}>
            <div>
              <p style={{ fontWeight: 800 }}>1. Enter symptoms</p>
              <p style={{ color: 'var(--text-muted)' }}>Write symptoms in simple language. No medical jargon required.</p>
            </div>
            <div>
              <p style={{ fontWeight: 800 }}>2. Get safe first-aid advice</p>
              <p style={{ color: 'var(--text-muted)' }}>Receive severity level, first-aid steps, precautions, and warning signs.</p>
            </div>
            <div>
              <p style={{ fontWeight: 800 }}>3. Escalate only when needed</p>
              <p style={{ color: 'var(--text-muted)' }}>Book a specialist only if symptoms indicate moderate or high risk.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;

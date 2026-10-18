'use client';

import { FormEvent, useEffect, useState } from 'react';
import apiClient from '@/lib/api-client';
import { useAuth } from '@/hooks/use-auth';
import type { CurrentUser } from '@/types/api';

interface Doctor {
  id: number;
  name: string;
  email: string;
  specialization: string;
  phone: string | null;
}

interface MedicalQuery {
  id: number;
  patient_id: number;
  patient_name: string;
  doctor_id: number;
  doctor_name: string;
  title: string;
  description: string;
  answer: string | null;
  status: 'Pending' | 'Answered';
  created_at: string;
  updated_at: string;
}

interface AdminStats {
  total_doctors: number;
  total_patients: number;
  total_queries: number;
  pending_queries: number;
  answered_queries: number;
}

const fieldStyle: React.CSSProperties = { display: 'grid', gap: 7 };
const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '11px 13px',
  border: '1px solid var(--border-subtle)',
  borderRadius: 9,
  background: 'var(--bg-elevated)',
  color: 'var(--text-primary)',
};

export default function DashboardPage() {
  const { user } = useAuth();
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [queries, setQueries] = useState<MedicalQuery[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [filter, setFilter] = useState('All');
  const [answers, setAnswers] = useState<Record<number, string>>({});

  async function loadDashboard(role: string) {
    setLoading(true);
    setError('');
    try {
      if (role === 'admin') {
        const [doctorResponse, statsResponse] = await Promise.all([
          apiClient.get<Doctor[]>('/v1/admin/doctors'),
          apiClient.get<AdminStats>('/v1/admin/stats'),
        ]);
        setDoctors(doctorResponse.data);
        setStats(statsResponse.data);
      } else if (role === 'doctor') {
        const response = await apiClient.get<MedicalQuery[]>('/v1/doctor/queries');
        setQueries(response.data);
      } else if (role === 'patient') {
        const [queryResponse, doctorResponse] = await Promise.all([
          apiClient.get<MedicalQuery[]>('/v1/patient/queries'),
          apiClient.get<Doctor[]>('/v1/patient/doctors'),
        ]);
        setQueries(queryResponse.data);
        setDoctors(doctorResponse.data);
      }
    } catch {
      setError('Could not load your dashboard. Please refresh and try again.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (user) void loadDashboard(user.role);
  }, [user]);

  if (!user) return <div className="skeleton" style={{ height: 220 }} />;
  return (
    <section style={{ maxWidth: 1080, margin: '0 auto', display: 'grid', gap: 24 }}>
      <header>
        <p style={{ color: 'var(--brand-400)', fontWeight: 700, marginBottom: 5 }}>
          {user.role.toUpperCase()} PORTAL
        </p>
        <h1 style={{ fontSize: '1.7rem', marginBottom: 6 }}>Welcome, {user.full_name}</h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          {user.role === 'patient' && 'Ask a doctor a question and follow the response here.'}
          {user.role === 'doctor' && 'Review your assigned patient questions and provide guidance.'}
          {user.role === 'admin' && 'Manage your care team and doctor accounts.'}
        </p>
      </header>

      {error && <div className="alert alert-error" role="alert">{error}</div>}
      {notice && <div className="alert" role="status">{notice}</div>}

      {user.role === 'admin' && (
        <AdminDashboard
          doctors={doctors}
          stats={stats}
          loading={loading}
          onCreated={async () => {
            setNotice('Doctor account created.');
            await loadDashboard(user.role);
          }}
          onError={setError}
        />
      )}
      {user.role === 'doctor' && (
        <DoctorDashboard
          queries={queries}
          loading={loading}
          filter={filter}
          setFilter={setFilter}
          answers={answers}
          setAnswers={setAnswers}
          onAnswered={async () => {
            setNotice('Your response has been submitted.');
            await loadDashboard(user.role);
          }}
          onError={setError}
        />
      )}
      {user.role === 'patient' && (
        <PatientDashboard
          queries={queries}
          doctors={doctors}
          loading={loading}
          onCreated={async () => {
            setNotice('Your question has been sent to the doctor.');
            await loadDashboard(user.role);
          }}
          onError={setError}
        />
      )}
    </section>
  );
}

function AdminDashboard({
  doctors,
  stats,
  loading,
  onCreated,
  onError,
}: {
  doctors: Doctor[];
  stats: AdminStats | null;
  loading: boolean;
  onCreated: () => Promise<void>;
  onError: (message: string) => void;
}) {
  const [saving, setSaving] = useState(false);

  async function createDoctor(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    onError('');
    const data = new FormData(event.currentTarget);
    const form = event.currentTarget;
    try {
      await apiClient.post('/v1/admin/doctors', {
        name: data.get('name'),
        specialization: data.get('specialization'),
        email: data.get('email'),
        password: data.get('password'),
        phone: data.get('phone') || null,
      });
      form.reset();
      await onCreated();
    } catch {
      onError('Unable to create doctor. Check the details and ensure the email is not already used.');
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 12 }}>
        {[
          ['Doctors', stats?.total_doctors],
          ['Patients', stats?.total_patients],
          ['Queries', stats?.total_queries],
          ['Pending', stats?.pending_queries],
          ['Answered', stats?.answered_queries],
        ].map(([label, value]) => (
          <div className="card" key={label} style={{ padding: 18 }}>
            <div style={{ color: 'var(--text-muted)', fontSize: 13 }}>{label}</div>
            <strong style={{ display: 'block', fontSize: 24, marginTop: 5 }}>{loading ? '—' : value ?? 0}</strong>
          </div>
        ))}
      </div>
      <div className="card" style={{ padding: 24 }}>
        <h2 style={{ marginBottom: 18 }}>Create a doctor account</h2>
        <form onSubmit={createDoctor} style={{ display: 'grid', gap: 14, gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
          <label style={fieldStyle}>Doctor name<input style={inputStyle} name="name" required maxLength={255} /></label>
          <label style={fieldStyle}>Specialization<input style={inputStyle} name="specialization" required maxLength={255} /></label>
          <label style={fieldStyle}>Email<input style={inputStyle} name="email" type="email" required /></label>
          <label style={fieldStyle}>Initial password<input style={inputStyle} name="password" type="password" minLength={8} maxLength={72} required /></label>
          <label style={fieldStyle}>Phone (optional)<input style={inputStyle} name="phone" type="tel" maxLength={30} /></label>
          <button className="btn btn-primary" disabled={saving} style={{ alignSelf: 'end', minHeight: 42 }}>
            {saving ? 'Creating…' : 'Create doctor'}
          </button>
        </form>
      </div>
      <div className="card" style={{ padding: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
          <h2>Doctors</h2><span>{loading ? 'Loading…' : `${doctors.length} accounts`}</span>
        </div>
        {doctors.length === 0 && !loading ? <p>No doctor accounts yet.</p> : (
          <div style={{ display: 'grid', gap: 10 }}>
            {doctors.map((doctor) => <DoctorCard key={doctor.id} doctor={doctor} />)}
          </div>
        )}
      </div>
    </>
  );
}

function PatientDashboard({
  queries,
  doctors,
  loading,
  onCreated,
  onError,
}: {
  queries: MedicalQuery[];
  doctors: Doctor[];
  loading: boolean;
  onCreated: () => Promise<void>;
  onError: (message: string) => void;
}) {
  const [saving, setSaving] = useState(false);

  async function createQuery(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    onError('');
    const data = new FormData(event.currentTarget);
    const form = event.currentTarget;
    try {
      await apiClient.post('/v1/patient/queries', {
        doctor_id: Number(data.get('doctor_id')),
        title: data.get('title'),
        description: data.get('description'),
      });
      form.reset();
      await onCreated();
    } catch {
      onError('Unable to send your question. Please check the selected doctor and try again.');
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <div className="card" style={{ padding: 24 }}>
        <h2 style={{ marginBottom: 18 }}>Ask a doctor</h2>
        <form onSubmit={createQuery} style={{ display: 'grid', gap: 14 }}>
          <label style={fieldStyle}>Doctor
            <select style={inputStyle} name="doctor_id" required defaultValue="">
              <option value="" disabled>Select a doctor</option>
              {doctors.map((doctor) => <option key={doctor.id} value={doctor.id}>{doctor.name} — {doctor.specialization}</option>)}
            </select>
          </label>
          <label style={fieldStyle}>Question title<input style={inputStyle} name="title" required maxLength={255} /></label>
          <label style={fieldStyle}>Describe your question
            <textarea style={{ ...inputStyle, minHeight: 120, resize: 'vertical' }} name="description" required maxLength={10000} />
          </label>
          <button className="btn btn-primary" disabled={saving || doctors.length === 0} style={{ justifySelf: 'start' }}>
            {saving ? 'Sending…' : 'Send question'}
          </button>
        </form>
      </div>
      <QueryList queries={queries} loading={loading} role="patient" />
    </>
  );
}

function DoctorDashboard({
  queries,
  loading,
  filter,
  setFilter,
  answers,
  setAnswers,
  onAnswered,
  onError,
}: {
  queries: MedicalQuery[];
  loading: boolean;
  filter: string;
  setFilter: (value: string) => void;
  answers: Record<number, string>;
  setAnswers: (value: Record<number, string>) => void;
  onAnswered: () => Promise<void>;
  onError: (message: string) => void;
}) {
  const shown = queries.filter((query) => filter === 'All' || query.status === filter);

  async function submitAnswer(event: FormEvent<HTMLFormElement>, queryId: number) {
    event.preventDefault();
    onError('');
    try {
      await apiClient.put(`/v1/doctor/queries/${queryId}/answer`, { answer: answers[queryId] });
      setAnswers({ ...answers, [queryId]: '' });
      await onAnswered();
    } catch {
      onError('Unable to submit this response. Please try again.');
    }
  }

  return (
    <div className="card" style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16, alignItems: 'center', marginBottom: 18 }}>
        <h2>Patient questions</h2>
        <select style={{ ...inputStyle, width: 'auto' }} value={filter} onChange={(event) => setFilter(event.target.value)}>
          <option>All</option><option>Pending</option><option>Answered</option>
        </select>
      </div>
      {loading ? <p>Loading questions…</p> : shown.length === 0 ? <p>No questions in this filter.</p> : (
        <div style={{ display: 'grid', gap: 14 }}>
          {shown.map((query) => (
            <article key={query.id} style={{ padding: 18, border: '1px solid var(--border-subtle)', borderRadius: 12 }}>
              <QueryHeader query={query} role="doctor" />
              <p style={{ whiteSpace: 'pre-wrap', margin: '12px 0' }}>{query.description}</p>
              {query.answer ? <div className="alert">Response: {query.answer}</div> : (
                <form onSubmit={(event) => void submitAnswer(event, query.id)} style={{ display: 'grid', gap: 10 }}>
                  <textarea
                    style={{ ...inputStyle, minHeight: 100, resize: 'vertical' }}
                    value={answers[query.id] ?? ''}
                    onChange={(event) => setAnswers({ ...answers, [query.id]: event.target.value })}
                    placeholder="Write your response"
                    required
                    maxLength={10000}
                  />
                  <button className="btn btn-primary" style={{ justifySelf: 'start' }}>Submit response</button>
                </form>
              )}
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

function QueryList({ queries, loading, role }: { queries: MedicalQuery[]; loading: boolean; role: CurrentUser['role'] }) {
  return (
    <div className="card" style={{ padding: 24 }}>
      <h2 style={{ marginBottom: 18 }}>{role === 'patient' ? 'Your questions' : 'Questions'}</h2>
      {loading ? <p>Loading questions…</p> : queries.length === 0 ? <p>No questions have been sent yet.</p> : (
        <div style={{ display: 'grid', gap: 14 }}>
          {queries.map((query) => (
            <article key={query.id} style={{ padding: 18, border: '1px solid var(--border-subtle)', borderRadius: 12 }}>
              <QueryHeader query={query} role={role} />
              <p style={{ whiteSpace: 'pre-wrap', margin: '12px 0' }}>{query.description}</p>
              {query.answer && <div className="alert">Doctor response: {query.answer}</div>}
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

function QueryHeader({ query, role }: { query: MedicalQuery; role: CurrentUser['role'] }) {
  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
        <h3>{query.title}</h3>
        <span className={`badge ${query.status === 'Answered' ? 'badge-responded' : 'badge-pending'}`}>{query.status}</span>
      </div>
      <p style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 6 }}>
        {role === 'doctor' ? `From ${query.patient_name}` : `Dr. ${query.doctor_name}`}
        {' · '}{new Date(query.created_at).toLocaleString()}
      </p>
    </>
  );
}

function DoctorCard({ doctor }: { doctor: Doctor }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, padding: 14, border: '1px solid var(--border-subtle)', borderRadius: 10 }}>
      <div><strong>{doctor.name}</strong><div style={{ color: 'var(--text-secondary)' }}>{doctor.specialization}</div></div>
      <div style={{ textAlign: 'right', color: 'var(--text-muted)' }}>{doctor.email}<br />{doctor.phone ?? 'No phone'}</div>
    </div>
  );
}

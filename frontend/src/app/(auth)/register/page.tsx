'use client';

import { FormEvent, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/api-client';

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '11px 13px',
  border: '1px solid var(--border-subtle)',
  borderRadius: 9,
  background: 'var(--bg-elevated)',
  color: 'var(--text-primary)',
};

export default function PatientRegistrationPage() {
  const router = useRouter();
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  async function register(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setSaving(true);
    const data = new FormData(event.currentTarget);
    try {
      await apiClient.post('/v1/patient/register', {
        name: data.get('name'),
        email: data.get('email'),
        password: data.get('password'),
        age: Number(data.get('age')),
        gender: data.get('gender'),
        contact_details: data.get('contact_details'),
      });
      router.push('/login?registered=1');
    } catch {
      setError('Registration failed. Check the details or use a different email address.');
    } finally {
      setSaving(false);
    }
  }

  return (
    <main style={{ minHeight: '100dvh', display: 'grid', placeItems: 'center', padding: 24 }}>
      <section className="glass-card" style={{ width: '100%', maxWidth: 520, padding: 30 }}>
        <p style={{ color: 'var(--brand-400)', fontWeight: 700, fontSize: 12, letterSpacing: 2 }}>PATIENT PORTAL</p>
        <h1 style={{ margin: '8px 0' }}>Create your account</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 22 }}>Register to ask questions and receive doctor responses.</p>
        {error && <div className="alert alert-error" role="alert" style={{ marginBottom: 16 }}>{error}</div>}
        <form onSubmit={register} style={{ display: 'grid', gap: 14 }}>
          <label style={{ display: 'grid', gap: 7 }}>Full name<input style={inputStyle} name="name" autoComplete="name" required maxLength={255} /></label>
          <label style={{ display: 'grid', gap: 7 }}>Email<input style={inputStyle} name="email" type="email" autoComplete="email" required /></label>
          <label style={{ display: 'grid', gap: 7 }}>Password<input style={inputStyle} name="password" type="password" autoComplete="new-password" minLength={8} maxLength={72} required /></label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <label style={{ display: 'grid', gap: 7 }}>Age<input style={inputStyle} name="age" type="number" min="0" max="130" required /></label>
            <label style={{ display: 'grid', gap: 7 }}>Gender<input style={inputStyle} name="gender" required maxLength={50} /></label>
          </div>
          <label style={{ display: 'grid', gap: 7 }}>Contact details<input style={inputStyle} name="contact_details" autoComplete="tel" required maxLength={255} /></label>
          <button className="btn btn-primary" disabled={saving} style={{ justifyContent: 'center', padding: 12 }}>
            {saving ? 'Creating account…' : 'Create account'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 20, color: 'var(--text-secondary)' }}>
          Already registered? <Link href="/login" style={{ color: 'var(--brand-400)' }}>Sign in</Link>
        </p>
      </section>
    </main>
  );
}

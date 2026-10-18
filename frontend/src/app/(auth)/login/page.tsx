'use client';

import { FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';

export default function LoginPage() {
  const router = useRouter();
  const { login, loading } = useAuth();
  const [error, setError] = useState('');
  const [registered, setRegistered] = useState(false);

  useEffect(() => setRegistered(new URLSearchParams(window.location.search).get('registered') === '1'), []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    const data = new FormData(event.currentTarget);
    try {
      await login(String(data.get('email')), String(data.get('password')));
      router.push('/dashboard');
    } catch {
      setError('Invalid email or password. Please check your details and try again.');
    }
  }

  return (
    <main style={{ minHeight: '100dvh', display: 'grid', placeItems: 'center', padding: 24 }}>
      <section className="glass-card" style={{ width: '100%', maxWidth: 440, padding: 32 }}>
        <div style={{ textAlign: 'center', marginBottom: 26 }}>
          <div style={{ display: 'inline-grid', placeItems: 'center', width: 58, height: 58, borderRadius: 16, background: 'linear-gradient(135deg, var(--brand-500), var(--brand-700))', fontSize: 26, color: 'white' }}>+</div>
          <p style={{ marginTop: 16, color: 'var(--brand-400)', fontSize: 12, fontWeight: 700, letterSpacing: 2 }}>HUMAN DOCTOR MANAGEMENT</p>
          <h1 style={{ margin: '8px 0' }}>Welcome back</h1>
          <p style={{ color: 'var(--text-secondary)' }}>One sign-in for admins, doctors, and patients; your account opens the matching portal.</p>
        </div>
        {registered && <div className="alert" role="status" style={{ marginBottom: 16 }}>Account created. You can sign in now.</div>}
        {error && <div className="alert alert-error" role="alert" style={{ marginBottom: 16 }}>{error}</div>}
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 16 }}>
          <label style={{ display: 'grid', gap: 7 }}>Email address
            <input className="form-input" type="email" name="email" autoComplete="email" required />
          </label>
          <label style={{ display: 'grid', gap: 7 }}>Password
            <input className="form-input" type="password" name="password" autoComplete="current-password" required />
          </label>
          <button className="btn btn-primary" type="submit" disabled={loading} style={{ justifyContent: 'center', padding: 12 }}>
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 20, color: 'var(--text-secondary)' }}>
          New patient? <Link href="/register" style={{ color: 'var(--brand-400)' }}>Create an account</Link>
        </p>
      </section>
    </main>
  );
}

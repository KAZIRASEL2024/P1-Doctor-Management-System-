import Link from 'next/link';

export default function NotFound() {
  return (
    <div style={{
      minHeight: '100dvh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center', gap: '16px', padding: '24px', textAlign: 'center',
    }}>
      <div style={{ fontSize: '4rem', fontWeight: 800, color: 'var(--brand-600)', lineHeight: 1 }}>404</div>
      <h2 style={{ color: 'var(--text-primary)' }}>Page not found</h2>
      <p>The page you are looking for does not exist.</p>
      <Link href="/dashboard" className="btn btn-primary">Go to Dashboard</Link>
    </div>
  );
}

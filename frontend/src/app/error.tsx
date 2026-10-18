'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div style={{
      minHeight: '100dvh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center', gap: '16px', padding: '24px', textAlign: 'center',
    }}>
      <div style={{ fontSize: '3rem' }}>⚠️</div>
      <h2 style={{ color: 'var(--text-primary)' }}>Something went wrong</h2>
      <p style={{ maxWidth: '400px' }}>{error.message || 'An unexpected error occurred.'}</p>
      <button className="btn btn-primary" onClick={reset}>Try again</button>
    </div>
  );
}

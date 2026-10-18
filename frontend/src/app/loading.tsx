export default function Loading() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', padding: '4px' }}>
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="skeleton" style={{ height: '160px', borderRadius: 'var(--radius-lg)' }} />
      ))}
    </div>
  );
}

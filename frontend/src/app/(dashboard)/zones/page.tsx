'use client';

import { useEffect, useState } from 'react';
import { MapPin, Users, Stethoscope, Tag } from 'lucide-react';
import apiClient from '@/lib/api-client';
import type { ZoneListResponse, Zone } from '@/types/zone';

function ZoneCard({ zone, index }: { zone: Zone; index: number }) {
  return (
    <div
      className={`card animate-fadeIn stagger-${Math.min(index + 1, 5)}`}
      style={{
        '--card-accent': zone.is_active ? 'hsl(142,70%,50%)' : 'hsl(215,20%,45%)',
        '--icon-bg': zone.is_active ? 'hsl(142,70%,6%)' : 'hsl(215,20%,10%)',
      } as React.CSSProperties}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '42px', height: '42px', borderRadius: 'var(--radius-md)',
            background: zone.is_active ? 'hsl(142,70%,6%)' : 'hsl(215,20%,10%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: zone.is_active ? 'hsl(142,70%,50%)' : 'var(--text-muted)',
          }}>
            <MapPin size={20} />
          </div>
          <div>
            <h3 style={{ color: 'var(--text-primary)', marginBottom: '2px' }}>{zone.name}</h3>
            {zone.erp_region_code && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <Tag size={11} /> ERP: {zone.erp_region_code}
              </div>
            )}
          </div>
        </div>
        <span className={`badge ${zone.is_active ? 'badge-responded' : 'badge-closed'}`} style={{ fontSize: '0.625rem' }}>
          {zone.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>

      {zone.description && (
        <p style={{ fontSize: '0.8125rem', marginBottom: '16px', lineHeight: 1.6 }}>{zone.description}</p>
      )}

      <div style={{ paddingTop: '16px', borderTop: '1px solid var(--border-subtle)', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Users size={14} style={{ color: 'var(--text-muted)' }} />
          <div>
            <div style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1 }}>{zone.doctor_count}</div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Doctors</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Stethoscope size={14} style={{ color: 'var(--text-muted)' }} />
          <div>
            <div style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1 }}>{zone.consultation_count}</div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Cases</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ZonesPage() {
  const [data, setData]       = useState<ZoneListResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get<ZoneListResponse>('/zones')
      .then(r => setData(r.data))
      .finally(() => setLoading(false));
  }, []);

  const activeCount   = data?.items.filter(z => z.is_active).length ?? 0;
  const totalDoctors  = data?.items.reduce((s, z) => s + z.doctor_count, 0) ?? 0;
  const totalCases    = data?.items.reduce((s, z) => s + z.consultation_count, 0) ?? 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      <div>
        <h1 style={{ marginBottom: '4px' }}>Geographic Zones</h1>
        <p>BRAC AISP operational zones aligned with ERP region codes.</p>
      </div>

      {/* Summary stats */}
      {!loading && data && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '14px' }}>
          {[
            { label: 'Total Zones',    value: data.total,   color: 'hsl(213,91%,60%)' },
            { label: 'Active Zones',   value: activeCount,  color: 'hsl(142,70%,50%)' },
            { label: 'Total Doctors',  value: totalDoctors, color: 'hsl(270,91%,65%)' },
            { label: 'Total Cases',    value: totalCases,   color: 'hsl(43,96%,56%)'  },
          ].map(({ label, value, color }) => (
            <div key={label} className="stat-card" style={{ '--card-accent': color } as React.CSSProperties}>
              <div className="stat-value" style={{ color }}>{value}</div>
              <div className="stat-label">{label}</div>
            </div>
          ))}
        </div>
      )}

      {/* ERP note */}
      <div className="alert alert-info" style={{ fontSize: '0.8125rem' }}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        ERP region code alignment is pending. Codes are stored for future integration with the BRAC ERP system.
      </div>

      {/* Zone grid */}
      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
          {Array.from({ length: 6 }).map((_, i) => <div key={i} className="skeleton" style={{ height: '180px', borderRadius: 'var(--radius-lg)' }} />)}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
          {data?.items.map((zone, i) => (
            <ZoneCard key={zone.id} zone={zone} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}

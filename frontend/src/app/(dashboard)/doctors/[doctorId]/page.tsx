'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Phone, Mail, MapPin, Stethoscope, Shield } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { getApiErrorMessage } from '@/lib/utils';
import type { Doctor } from '@/types/doctor';

export default function DoctorDetailPage() {
  const { doctorId } = useParams<{ doctorId: string }>();
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    apiClient.get<Doctor>(`/doctors/${doctorId}`)
      .then(r => setDoctor(r.data))
      .catch(err => setError(getApiErrorMessage(err, 'Doctor profile not found.')))
      .finally(() => setLoading(false));
  }, [doctorId]);

  if (loading) return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {Array.from({ length: 2 }).map((_, i) => <div key={i} className="skeleton" style={{ height: '200px', borderRadius: 'var(--radius-lg)' }} />)}
    </div>
  );

  if (error || !doctor) return <div className="alert alert-error" role="alert">{error || 'Doctor profile not found.'}</div>;

  const initials = doctor.full_name.split(' ').slice(0, 2).map(p => p[0]).join('').toUpperCase();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '760px' }} className="animate-fadeIn">
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <Link href="/doctors" className="btn btn-ghost" style={{ padding: '8px' }}>
          <ArrowLeft size={18} />
        </Link>
        <h1>Doctor Profile</h1>
      </div>

      {/* Profile card */}
      <div className="card">
        <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start', marginBottom: '24px' }}>
          <div className="avatar-placeholder" style={{ width: '72px', height: '72px', fontSize: '1.5rem' }}>{initials}</div>
          <div style={{ flex: 1 }}>
            <h2 style={{ marginBottom: '4px' }}>{doctor.full_name}</h2>
            <p style={{ color: 'var(--brand-400)', fontWeight: 500, marginBottom: '8px' }}>{doctor.specialization}</p>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {doctor.is_emergency_doctor && <span className="badge badge-emergency">🚨 Emergency Doctor</span>}
              <span className={`badge ${doctor.is_available ? 'badge-responded' : 'badge-closed'}`}>
                {doctor.is_available ? 'Available' : 'Unavailable'}
              </span>
            </div>
          </div>
        </div>

        <div className="divider" style={{ margin: '0 0 20px' }} />

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Registration</div>
            <div style={{ fontFamily: 'monospace', color: 'var(--text-primary)' }}>{doctor.registration_number}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Qualification</div>
            <div style={{ color: 'var(--text-primary)' }}>{doctor.qualification}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Phone</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-primary)' }}>
              <Phone size={14} style={{ color: 'var(--text-muted)' }} /> {doctor.phone}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Email</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-primary)' }}>
              <Mail size={14} style={{ color: 'var(--text-muted)' }} /> {doctor.email}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Total Responses</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--brand-400)', fontWeight: 700, fontSize: '1.25rem' }}>
              <Stethoscope size={18} /> {doctor.total_responses}
            </div>
          </div>
        </div>

        {doctor.bio && (
          <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '8px' }}>About</div>
            <p style={{ lineHeight: 1.7 }}>{doctor.bio}</p>
          </div>
        )}
      </div>

      {/* Assigned zones */}
      <div className="card">
        <h3 style={{ marginBottom: '16px' }}>
          <MapPin size={16} style={{ display: 'inline', marginRight: '8px' }} />
          Assigned Zones ({doctor.zones.length})
        </h3>
        {doctor.zones.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>No zones assigned.</p>
        ) : (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {doctor.zones.map(z => (
              <div key={z.id} style={{
                padding: '10px 16px',
                background: 'var(--bg-elevated)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-subtle)',
                fontSize: '0.875rem',
                color: 'var(--text-primary)',
                fontWeight: 500,
              }}>
                <MapPin size={13} style={{ display: 'inline', marginRight: '6px', color: 'var(--brand-400)' }} />
                {z.name}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

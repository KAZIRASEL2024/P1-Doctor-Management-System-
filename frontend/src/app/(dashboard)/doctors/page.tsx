'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Phone, Mail, Stethoscope, MapPin, Plus, ArrowUpRight } from 'lucide-react';
import apiClient from '@/lib/api-client';
import type { DoctorListResponse, Doctor } from '@/types/doctor';
import { getStoredUser } from '@/lib/auth';

function DoctorCard({ doctor }: { doctor: Doctor }) {
  const initials = doctor.full_name.split(' ').slice(0, 2).map(p => p[0]).join('').toUpperCase();
  return (
    <Link href={`/doctors/${doctor.id}`} style={{ textDecoration: 'none' }}>
      <div className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }}
        onMouseEnter={e => (e.currentTarget.style.transform = 'translateY(-2px)')}
        onMouseLeave={e => (e.currentTarget.style.transform = '')}>
        {/* Card top accent stripe handled by CSS */}
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px', marginBottom: '16px' }}>
          <div className="avatar-placeholder" style={{ width: '56px', height: '56px', fontSize: '1.125rem', flexShrink: 0 }}>
            {initials}
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <h3 style={{ color: 'var(--text-primary)', marginBottom: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {doctor.full_name}
            </h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--brand-400)', fontWeight: 500, marginBottom: '0' }}>
              {doctor.specialization}
            </p>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', alignItems: 'flex-end' }}>
            {doctor.is_emergency_doctor && (
              <span className="badge badge-emergency" style={{ fontSize: '0.625rem' }}>🚨 Emergency</span>
            )}
            <span className={`badge ${doctor.is_available ? 'badge-responded' : 'badge-closed'}`} style={{ fontSize: '0.625rem' }}>
              {doctor.is_available ? '● Available' : '○ Unavailable'}
            </span>
          </div>
        </div>

        <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
          {doctor.qualification}
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8125rem' }}>
            <Phone size={13} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
            <span style={{ color: 'var(--text-secondary)' }}>{doctor.phone}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8125rem' }}>
            <Mail size={13} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
            <span style={{ color: 'var(--text-secondary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doctor.email}</span>
          </div>
        </div>

        {doctor.zones.length > 0 && (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
            {doctor.zones.slice(0, 3).map(z => (
              <span key={z.id} style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', padding: '3px 8px', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-full)', fontSize: '0.6875rem', color: 'var(--text-muted)', border: '1px solid var(--border-subtle)' }}>
                <MapPin size={10} /> {z.name}
              </span>
            ))}
            {doctor.zones.length > 3 && (
              <span style={{ padding: '3px 8px', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-full)', fontSize: '0.6875rem', color: 'var(--text-muted)', border: '1px solid var(--border-subtle)' }}>
                +{doctor.zones.length - 3} more
              </span>
            )}
          </div>
        )}

        <div style={{ paddingTop: '12px', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>Reg. {doctor.registration_number}</span>
          <span style={{ color: 'var(--brand-400)', fontWeight: 600 }}>
            <Stethoscope size={13} style={{ display: 'inline', marginRight: '4px' }} />
            {doctor.total_responses} responses
          </span>
        </div>
        <div style={{ marginTop: '12px', color: 'var(--brand-400)', fontSize: '0.8125rem', fontWeight: 600 }}>
          View profile <ArrowUpRight size={14} style={{ display: 'inline', verticalAlign: 'middle' }} />
        </div>
      </div>
    </Link>
  );
}

export default function DoctorsPage() {
  const [data, setData]     = useState<DoctorListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    setIsAdmin(getStoredUser()?.role === 'admin');
  }, []);

  useEffect(() => {
    apiClient.get<DoctorListResponse>('/doctors')
      .then(r => setData(r.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
        <div>
          <h1 style={{ marginBottom: '4px' }}>Veterinary Doctors</h1>
          <p>{data?.total ?? 0} doctor{data?.total !== 1 ? 's' : ''} registered</p>
        </div>
        {isAdmin && (
          <Link href="/doctors/new" className="btn btn-primary">
            <Plus size={16} /> Create Doctor
          </Link>
        )}
      </div>

      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
          {Array.from({ length: 4 }).map((_, i) => <div key={i} className="skeleton" style={{ height: '240px', borderRadius: 'var(--radius-lg)' }} />)}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
          {data?.items.map((doc, i) => (
            <div key={doc.id} className={`animate-fadeIn stagger-${Math.min(i + 1, 5)}`}>
              <DoctorCard doctor={doc} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

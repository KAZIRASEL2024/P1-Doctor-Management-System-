'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ArrowLeft, CalendarDays, MapPin, PawPrint, Phone, Scale, UserRound } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { formatDate, getApiErrorMessage } from '@/lib/utils';
import type { Patient } from '@/types/patient';

function formatAge(months: number | null): string {
  if (months === null) return 'Not specified';
  const years = Math.floor(months / 12);
  const remainingMonths = months % 12;
  if (years === 0) return `${remainingMonths} month${remainingMonths === 1 ? '' : 's'}`;
  if (remainingMonths === 0) return `${years} year${years === 1 ? '' : 's'}`;
  return `${years}y ${remainingMonths}m`;
}

export default function PatientProfilePage() {
  const { patientId } = useParams<{ patientId: string }>();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    apiClient.get<Patient>(`/patients/${patientId}`)
      .then(response => setPatient(response.data))
      .catch(err => setError(getApiErrorMessage(err, 'Patient profile not found.')))
      .finally(() => setLoading(false));
  }, [patientId]);

  if (loading) return <div className="skeleton" style={{ height: '320px', borderRadius: 'var(--radius-lg)' }} />;
  if (error || !patient) return <div className="alert alert-error" role="alert">{error || 'Patient profile not found.'}</div>;

  const details = [
    { label: 'Species', value: patient.species },
    { label: 'Breed', value: patient.breed || 'Not specified' },
    { label: 'Sex', value: patient.sex ? patient.sex[0].toUpperCase() + patient.sex.slice(1) : 'Not specified' },
    { label: 'Age', value: formatAge(patient.age_months) },
    { label: 'Weight', value: patient.weight_kg === null ? 'Not specified' : `${patient.weight_kg} kg` },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '840px' }} className="animate-fadeIn">
      <div>
        <Link href="/patients" className="btn btn-ghost" style={{ paddingLeft: 0, marginBottom: '12px' }}>
          <ArrowLeft size={16} /> Back to patients
        </Link>
        <h1 style={{ marginBottom: '4px' }}>Patient Profile</h1>
        <p>Registered {formatDate(patient.created_at)}</p>
      </div>

      <section className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
          <div className="avatar-placeholder" style={{ width: '64px', height: '64px' }}><PawPrint size={28} /></div>
          <div>
            <h2 style={{ marginBottom: '4px' }}>{patient.name}</h2>
            <p style={{ color: 'var(--brand-400)', margin: 0 }}>{patient.species}{patient.breed ? ` · ${patient.breed}` : ''}</p>
          </div>
        </div>
        <div className="divider" style={{ margin: '0 0 20px' }} />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '20px' }}>
          {details.map(({ label, value }) => (
            <div key={label}>
              <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '5px' }}>{label}</div>
              <div style={{ color: 'var(--text-primary)' }}>{value}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '18px' }}><UserRound size={17} /> Owner information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          <div style={{ color: 'var(--text-primary)' }}><UserRound size={15} style={{ verticalAlign: 'middle', marginRight: '8px', color: 'var(--text-muted)' }} />{patient.owner_name}</div>
          <div style={{ color: 'var(--text-primary)' }}><Phone size={15} style={{ verticalAlign: 'middle', marginRight: '8px', color: 'var(--text-muted)' }} />{patient.owner_phone || 'No phone provided'}</div>
          <div style={{ color: 'var(--text-primary)' }}><MapPin size={15} style={{ verticalAlign: 'middle', marginRight: '8px', color: 'var(--text-muted)' }} />{patient.location || 'No location provided'}</div>
        </div>
      </section>

      <section className="card">
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}><Scale size={17} /> Medical notes</h3>
        <p style={{ lineHeight: 1.7, whiteSpace: 'pre-wrap', margin: 0, color: patient.medical_notes ? 'var(--text-secondary)' : 'var(--text-muted)' }}>
          {patient.medical_notes || 'No medical notes recorded.'}
        </p>
      </section>
    </div>
  );
}

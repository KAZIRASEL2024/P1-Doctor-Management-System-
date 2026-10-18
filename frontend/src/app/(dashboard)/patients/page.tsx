'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowUpRight, PawPrint, Plus, UserRound } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { getApiErrorMessage } from '@/lib/utils';
import type { Patient, PatientListResponse } from '@/types/patient';

function PatientCard({ patient }: { patient: Patient }) {
  return (
    <Link href={`/patients/${patient.id}`} style={{ textDecoration: 'none' }}>
      <article className="card" style={{ height: '100%', transition: 'transform 0.2s' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '16px' }}>
          <div className="stat-icon" style={{ color: 'var(--brand-400)' }}><PawPrint size={22} /></div>
          <div style={{ minWidth: 0 }}>
            <h3 style={{ color: 'var(--text-primary)', marginBottom: '3px' }}>{patient.name}</h3>
            <p style={{ color: 'var(--brand-400)', margin: 0 }}>{patient.species}{patient.breed ? ` · ${patient.breed}` : ''}</p>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          <UserRound size={14} /> Owner: {patient.owner_name}
        </div>
        {patient.owner_phone && <p style={{ fontSize: '0.8125rem', margin: '8px 0 0 22px' }}>{patient.owner_phone}</p>}
        <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid var(--border-subtle)', color: 'var(--brand-400)', fontSize: '0.8125rem', fontWeight: 600 }}>
          View profile <ArrowUpRight size={14} style={{ display: 'inline', verticalAlign: 'middle' }} />
        </div>
      </article>
    </Link>
  );
}

export default function PatientsPage() {
  const [data, setData] = useState<PatientListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    apiClient.get<PatientListResponse>('/patients')
      .then(response => setData(response.data))
      .catch(err => setError(getApiErrorMessage(err, 'Unable to load patients.')))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
        <div>
          <h1 style={{ marginBottom: '4px' }}>Animal Patients</h1>
          <p>{data?.total ?? 0} patient{data?.total !== 1 ? 's' : ''} registered</p>
        </div>
        <Link href="/patients/new" className="btn btn-primary"><Plus size={16} /> Create Patient</Link>
      </div>

      {error && <div className="alert alert-error" role="alert">{error}</div>}
      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
          {Array.from({ length: 4 }).map((_, index) => <div key={index} className="skeleton" style={{ height: '180px', borderRadius: 'var(--radius-lg)' }} />)}
        </div>
      ) : data?.items.length ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
          {data.items.map(patient => <PatientCard key={patient.id} patient={patient} />)}
        </div>
      ) : !error ? (
        <div className="card empty-state">
          <PawPrint size={42} />
          <p>No patients registered yet.</p>
          <Link href="/patients/new" className="btn btn-primary"><Plus size={16} /> Create the first patient</Link>
        </div>
      ) : null}
    </div>
  );
}

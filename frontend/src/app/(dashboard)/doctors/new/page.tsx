'use client';

import { type FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Plus } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { getStoredUser } from '@/lib/auth';
import { getApiErrorMessage } from '@/lib/utils';
import type { DoctorCreate, Doctor } from '@/types/doctor';
import type { ZoneListResponse } from '@/types/zone';

const initialForm: DoctorCreate = {
  full_name: '',
  email: '',
  password: '',
  registration_number: '',
  specialization: '',
  qualification: '',
  phone: '',
  bio: '',
  is_emergency_doctor: false,
  is_available: true,
  zone_ids: [],
};

export default function CreateDoctorPage() {
  const router = useRouter();
  const [form, setForm] = useState(initialForm);
  const [zones, setZones] = useState<ZoneListResponse['items']>([]);
  const [authorized, setAuthorized] = useState(false);
  const [loadingZones, setLoadingZones] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (getStoredUser()?.role !== 'admin') {
      router.replace('/doctors');
      return;
    }
    setAuthorized(true);
    apiClient.get<ZoneListResponse>('/zones')
      .then(response => setZones(response.data.items))
      .catch(err => setError(getApiErrorMessage(err, 'Unable to load zones.')))
      .finally(() => setLoadingZones(false));
  }, [router]);

  function update<K extends keyof DoctorCreate>(key: K, value: DoctorCreate[K]) {
    setForm(current => ({ ...current, [key]: value }));
  }

  function toggleZone(zoneId: number) {
    setForm(current => ({
      ...current,
      zone_ids: current.zone_ids.includes(zoneId)
        ? current.zone_ids.filter(id => id !== zoneId)
        : [...current.zone_ids, zoneId],
    }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError('');
    try {
      const response = await apiClient.post<Doctor>('/doctors', form);
      router.push(`/doctors/${response.data.id}`);
    } catch (err) {
      setError(getApiErrorMessage(err, 'Unable to create doctor.'));
    } finally {
      setSaving(false);
    }
  }

  if (!authorized) return <div className="skeleton" style={{ height: '320px', borderRadius: 'var(--radius-lg)' }} />;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '820px' }}>
      <div>
        <Link href="/doctors" className="btn btn-ghost" style={{ paddingLeft: 0, marginBottom: '12px' }}>
          <ArrowLeft size={16} /> Back to doctors
        </Link>
        <h1 style={{ marginBottom: '4px' }}>Create Doctor</h1>
        <p>Register a veterinary doctor and set up their account.</p>
      </div>

      <form className="card" onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {error && <div className="alert alert-error" role="alert">{error}</div>}

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
          <div className="form-group">
            <label className="form-label" htmlFor="full_name">Full name *</label>
            <input id="full_name" className="form-input" value={form.full_name} onChange={e => update('full_name', e.target.value)} required maxLength={255} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Email address *</label>
            <input id="email" type="email" className="form-input" value={form.email} onChange={e => update('email', e.target.value)} required maxLength={255} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="password">Temporary password *</label>
            <input id="password" type="password" className="form-input" value={form.password} onChange={e => update('password', e.target.value)} required minLength={8} maxLength={128} autoComplete="new-password" />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="registration_number">Registration number *</label>
            <input id="registration_number" className="form-input" value={form.registration_number} onChange={e => update('registration_number', e.target.value)} required maxLength={100} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="specialization">Specialization *</label>
            <input id="specialization" className="form-input" value={form.specialization} onChange={e => update('specialization', e.target.value)} required maxLength={255} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="qualification">Qualification *</label>
            <input id="qualification" className="form-input" value={form.qualification} onChange={e => update('qualification', e.target.value)} required maxLength={255} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="phone">Phone *</label>
            <input id="phone" type="tel" className="form-input" value={form.phone} onChange={e => update('phone', e.target.value)} required maxLength={30} />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="bio">About the doctor</label>
          <textarea id="bio" className="form-textarea" value={form.bio} onChange={e => update('bio', e.target.value)} rows={4} />
        </div>

        <fieldset style={{ border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '16px' }}>
          <legend style={{ padding: '0 6px', color: 'var(--text-secondary)', fontWeight: 600 }}>Assigned zones</legend>
          {loadingZones ? (
            <p>Loading zones…</p>
          ) : zones.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>No zones are available.</p>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
              {zones.map(zone => (
                <label key={zone.id} style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
                  <input type="checkbox" checked={form.zone_ids.includes(zone.id)} onChange={() => toggleZone(zone.id)} />
                  {zone.name}
                </label>
              ))}
            </div>
          )}
        </fieldset>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
            <input type="checkbox" checked={form.is_emergency_doctor} onChange={e => update('is_emergency_doctor', e.target.checked)} />
            Emergency doctor
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
            <input type="checkbox" checked={form.is_available} onChange={e => update('is_available', e.target.checked)} />
            Available for consultations
          </label>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
          <Link href="/doctors" className="btn btn-secondary">Cancel</Link>
          <button type="submit" className="btn btn-primary" disabled={saving || loadingZones}>
            <Plus size={16} /> {saving ? 'Creating…' : 'Create Doctor'}
          </button>
        </div>
      </form>
    </div>
  );
}

'use client';

import { type FormEvent, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Plus } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { getApiErrorMessage } from '@/lib/utils';
import type { Patient, PatientCreate } from '@/types/patient';

const initialForm: PatientCreate = {
  name: '',
  species: '',
  breed: '',
  sex: '',
  age_months: null,
  weight_kg: null,
  owner_name: '',
  owner_phone: '',
  location: '',
  medical_notes: '',
};

export default function CreatePatientPage() {
  const router = useRouter();
  const [form, setForm] = useState(initialForm);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError('');
    try {
      const response = await apiClient.post<Patient>('/patients', form);
      router.push(`/patients/${response.data.id}`);
    } catch (err) {
      setError(getApiErrorMessage(err, 'Unable to create patient.'));
    } finally {
      setSaving(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '820px' }}>
      <div>
        <Link href="/patients" className="btn btn-ghost" style={{ paddingLeft: 0, marginBottom: '12px' }}>
          <ArrowLeft size={16} /> Back to patients
        </Link>
        <h1 style={{ marginBottom: '4px' }}>Create Patient</h1>
        <p>Register an animal and its owner to create a patient profile.</p>
      </div>

      <form className="card" onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {error && <div className="alert alert-error" role="alert">{error}</div>}

        <h3 style={{ marginBottom: '-8px' }}>Animal information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">Animal name / identifier *</label>
            <input id="name" className="form-input" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required maxLength={255} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="species">Species *</label>
            <input id="species" className="form-input" value={form.species} onChange={e => setForm({ ...form, species: e.target.value })} required maxLength={100} placeholder="e.g. Cattle, Goat, Poultry" />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="breed">Breed</label>
            <input id="breed" className="form-input" value={form.breed ?? ''} onChange={e => setForm({ ...form, breed: e.target.value })} maxLength={100} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="sex">Sex</label>
            <select id="sex" className="form-select" value={form.sex ?? ''} onChange={e => setForm({ ...form, sex: e.target.value || null })}>
              <option value="">Not specified</option>
              <option value="female">Female</option>
              <option value="male">Male</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="age_months">Age (months)</label>
            <input id="age_months" type="number" min="0" step="1" className="form-input" value={form.age_months ?? ''} onChange={e => setForm({ ...form, age_months: e.target.value ? Number(e.target.value) : null })} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="weight_kg">Weight (kg)</label>
            <input id="weight_kg" type="number" min="0.01" step="0.01" className="form-input" value={form.weight_kg ?? ''} onChange={e => setForm({ ...form, weight_kg: e.target.value ? Number(e.target.value) : null })} />
          </div>
        </div>

        <h3 style={{ marginBottom: '-8px' }}>Owner information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          <div className="form-group">
            <label className="form-label" htmlFor="owner_name">Owner name *</label>
            <input id="owner_name" className="form-input" value={form.owner_name} onChange={e => setForm({ ...form, owner_name: e.target.value })} required maxLength={255} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="owner_phone">Owner phone</label>
            <input id="owner_phone" type="tel" className="form-input" value={form.owner_phone ?? ''} onChange={e => setForm({ ...form, owner_phone: e.target.value })} maxLength={30} />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="location">Location</label>
            <input id="location" className="form-input" value={form.location ?? ''} onChange={e => setForm({ ...form, location: e.target.value })} maxLength={255} />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="medical_notes">Medical notes</label>
          <textarea id="medical_notes" className="form-textarea" value={form.medical_notes ?? ''} onChange={e => setForm({ ...form, medical_notes: e.target.value })} rows={4} placeholder="Known conditions, allergies, or other relevant information" />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
          <Link href="/patients" className="btn btn-secondary">Cancel</Link>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            <Plus size={16} /> {saving ? 'Creating…' : 'Create Patient'}
          </button>
        </div>
      </form>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import {
  ArrowLeft, Thermometer, Weight, Clock, User, MapPin,
  Paperclip, CheckCircle2, AlertTriangle, Image, Mic, FileText,
  Phone, Tag
} from 'lucide-react';
import apiClient from '@/lib/api-client';
import type { ConsultationDetail, ResponseSubmit } from '@/types/consultation';
import { formatDate, formatRelativeTime, statusLabel, priorityLabel, formatFileSize } from '@/lib/utils';

function DetailRow({ label, value, icon: Icon }: { label: string; value: React.ReactNode; icon?: React.ElementType }) {
  if (!value && value !== 0) return null;
  return (
    <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
      {Icon && <Icon size={16} style={{ color: 'var(--text-muted)', marginTop: '2px', flexShrink: 0 }} />}
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '2px' }}>
          {label}
        </div>
        <div style={{ fontSize: '0.9375rem', color: 'var(--text-primary)' }}>{value}</div>
      </div>
    </div>
  );
}

const fileTypeIcon = (ft: string) =>
  ft === 'photo' ? <Image size={16} /> : ft === 'audio' ? <Mic size={16} /> : <FileText size={16} />;

export default function ConsultationDetailPage() {
  const { consultationId } = useParams<{ consultationId: string }>();
  const router = useRouter();

  const [data, setData]       = useState<ConsultationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState('');

  // Response form state
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [form, setForm] = useState<ResponseSubmit>({
    consultation_id: Number(consultationId),
    diagnosis: '',
    treatment_plan: '',
    medications: '',
    follow_up_instructions: '',
    is_emergency_referral: false,
  });

  useEffect(() => {
    setLoading(true);
    apiClient.get<ConsultationDetail>(`/consultations/${consultationId}`)
      .then(r => { setData(r.data); setForm(f => ({ ...f, consultation_id: r.data.id })); })
      .catch(() => setError('Failed to load consultation.'))
      .finally(() => setLoading(false));
  }, [consultationId]);

  async function handleSubmitResponse(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setSubmitError('');
    try {
      await apiClient.post('/responses', form);
      setSubmitSuccess(true);
      // Refresh data
      const r = await apiClient.get<ConsultationDetail>(`/consultations/${consultationId}`);
      setData(r.data);
    } catch (err: any) {
      setSubmitError(err.response?.data?.error ?? 'Failed to submit response.');
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {Array.from({ length: 3 }).map((_, i) => <div key={i} className="skeleton" style={{ height: '200px', borderRadius: 'var(--radius-lg)' }} />)}
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="empty-state">
        <AlertTriangle size={48} />
        <p>{error || 'Consultation not found.'}</p>
        <button className="btn btn-secondary" onClick={() => router.back()}>Go Back</button>
      </div>
    );
  }

  const hasResponse = data.responses.length > 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '900px' }} className="animate-fadeIn">
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button className="btn btn-ghost" style={{ padding: '8px' }} onClick={() => router.back()}>
          <ArrowLeft size={18} />
        </button>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
            <h1 style={{ fontSize: '1.25rem' }}>{data.aisp_reference ?? `Consultation #${data.id}`}</h1>
            <span className={`badge badge-${data.priority}`}>{priorityLabel(data.priority)}</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <div className={`status-dot ${data.status}`} />
              <span className={`badge badge-${data.status}`}>{statusLabel(data.status)}</span>
            </div>
          </div>
          <p style={{ fontSize: '0.8125rem', marginTop: '4px' }}>
            Submitted {formatRelativeTime(data.submitted_at)} · {formatDate(data.submitted_at)}
          </p>
        </div>
      </div>

      {/* Overdue warning */}
      {data.sla_deadline && new Date(data.sla_deadline) < new Date() && data.status !== 'responded' && (
        <div className="alert alert-error">
          <AlertTriangle size={16} />
          SLA deadline passed {formatRelativeTime(data.sla_deadline)}. This case is overdue.
        </div>
      )}

      {/* Main grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Left: Animal & field info */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
          <h3 style={{ marginBottom: '8px' }}>🐄 Animal Information</h3>
          <DetailRow label="Species"      value={data.animal_species}          />
          <DetailRow label="Breed"        value={data.animal_breed}            />
          <DetailRow label="Age"          value={data.animal_age_months ? `${data.animal_age_months} months` : undefined} icon={Clock} />
          <DetailRow label="Weight"       value={data.animal_weight_kg ? `${data.animal_weight_kg} kg` : undefined} icon={Weight} />
          <DetailRow label="Temperature"  value={data.animal_temperature_celsius ? `${data.animal_temperature_celsius} °C` : undefined} icon={Thermometer} />
          <DetailRow label="Owner"        value={data.animal_owner_name}       icon={User}  />
        </div>

        {/* Right: Case info */}
        <div className="card">
          <h3 style={{ marginBottom: '8px' }}>📋 Case Information</h3>
          <DetailRow label="Zone"         value={data.zone_name}               icon={MapPin} />
          <DetailRow label="Field Worker" value={data.field_worker_name}       icon={User}  />
          <DetailRow label="Contact"      value={data.field_worker_phone}      icon={Phone} />
          <DetailRow label="SLA Deadline" value={data.sla_deadline ? formatDate(data.sla_deadline) : 'Not set'} icon={Clock} />
        </div>
      </div>

      {/* Symptoms & Remarks */}
      <div className="card">
        <h3 style={{ marginBottom: '16px' }}>🩺 Clinical Presentation</h3>
        <div style={{ marginBottom: '16px' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '8px' }}>
            Symptoms
          </div>
          <div style={{ background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', padding: '16px', color: 'var(--text-primary)', lineHeight: 1.7 }}>
            {data.symptoms}
          </div>
        </div>
        {data.remarks && (
          <div>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '8px' }}>
              Field Worker Remarks
            </div>
            <div style={{ background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', padding: '16px', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
              {data.remarks}
            </div>
          </div>
        )}
      </div>

      {/* Attachments */}
      {data.attachments.length > 0 && (
        <div className="card">
          <h3 style={{ marginBottom: '16px' }}>
            <Paperclip size={16} style={{ display: 'inline', marginRight: '8px' }} />
            Attachments ({data.attachments.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {data.attachments.map(att => (
              <div key={att.id} style={{
                display: 'flex', alignItems: 'center', gap: '12px',
                padding: '12px 16px',
                background: 'var(--bg-elevated)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-subtle)',
              }}>
                <div style={{ color: 'var(--brand-400)' }}>{fileTypeIcon(att.file_type)}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '0.875rem', fontWeight: 500, color: 'var(--text-primary)' }}>{att.file_name}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{att.mime_type} · {formatFileSize(att.file_size_bytes)}</div>
                </div>
                <span className="badge badge-normal" style={{ fontSize: '0.625rem' }}>{att.file_type.toUpperCase()}</span>
              </div>
            ))}
          </div>
          <p style={{ fontSize: '0.75rem', marginTop: '12px', color: 'var(--text-muted)' }}>
            ⚠️ Demo mode: file download not available. In production, files are served from secure object storage.
          </p>
        </div>
      )}

      {/* Existing responses */}
      {hasResponse && (
        <div className="card">
          <h3 style={{ marginBottom: '16px' }}>
            <CheckCircle2 size={16} style={{ display: 'inline', marginRight: '8px', color: 'var(--status-responded)' }} />
            Doctor Response{data.responses.length > 1 ? 's' : ''}
          </h3>
          {data.responses.map(res => (
            <div key={res.id} style={{
              background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)',
              padding: '20px', marginBottom: '12px',
              border: '1px solid var(--border-subtle)',
            }}>
              {res.is_emergency_referral && (
                <div className="alert alert-error" style={{ marginBottom: '16px' }}>
                  <AlertTriangle size={14} /> This case requires emergency referral.
                </div>
              )}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div>
                  <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '6px' }}>Diagnosis</div>
                  <p style={{ color: 'var(--text-primary)', lineHeight: 1.6 }}>{res.diagnosis}</p>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '6px' }}>Treatment Plan</div>
                  <p style={{ color: 'var(--text-primary)', lineHeight: 1.6, whiteSpace: 'pre-line' }}>{res.treatment_plan}</p>
                </div>
                {res.medications && (
                  <div>
                    <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '6px' }}>Medications</div>
                    <p style={{ color: 'var(--text-primary)', lineHeight: 1.6 }}>{res.medications}</p>
                  </div>
                )}
                {res.follow_up_instructions && (
                  <div>
                    <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '6px' }}>Follow-up</div>
                    <p style={{ color: 'var(--text-primary)', lineHeight: 1.6 }}>{res.follow_up_instructions}</p>
                  </div>
                )}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '12px', paddingTop: '12px', borderTop: '1px solid var(--border-subtle)' }}>
                Responded {formatDate(res.created_at)}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Response form */}
      {!hasResponse || data.status === 'pending' || data.status === 'in_progress' ? (
        <div className="card">
          <h3 style={{ marginBottom: '20px' }}>✍️ Submit Your Response</h3>

          {submitSuccess && (
            <div className="alert alert-success" style={{ marginBottom: '16px' }}>
              <CheckCircle2 size={16} /> Response submitted successfully.
            </div>
          )}
          {submitError && (
            <div className="alert alert-error" style={{ marginBottom: '16px' }}>
              <AlertTriangle size={16} /> {submitError}
            </div>
          )}

          <form onSubmit={handleSubmitResponse} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
            <div className="form-group">
              <label className="form-label">Diagnosis *</label>
              <textarea
                className="form-textarea"
                style={{ minHeight: '100px' }}
                placeholder="Provide your clinical diagnosis based on the symptoms and findings…"
                value={form.diagnosis}
                onChange={e => setForm(f => ({ ...f, diagnosis: e.target.value }))}
                required
                minLength={10}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Treatment Plan *</label>
              <textarea
                className="form-textarea"
                style={{ minHeight: '120px' }}
                placeholder="Describe the treatment plan with step-by-step instructions…"
                value={form.treatment_plan}
                onChange={e => setForm(f => ({ ...f, treatment_plan: e.target.value }))}
                required
                minLength={10}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '18px' }}>
              <div className="form-group">
                <label className="form-label">Medications</label>
                <textarea
                  className="form-textarea"
                  style={{ minHeight: '80px' }}
                  placeholder="Drug name, dose, route, frequency…"
                  value={form.medications}
                  onChange={e => setForm(f => ({ ...f, medications: e.target.value }))}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Follow-up Instructions</label>
                <textarea
                  className="form-textarea"
                  style={{ minHeight: '80px' }}
                  placeholder="Monitoring, next visit, owner instructions…"
                  value={form.follow_up_instructions}
                  onChange={e => setForm(f => ({ ...f, follow_up_instructions: e.target.value }))}
                />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <input
                id="emergency-ref"
                type="checkbox"
                checked={form.is_emergency_referral}
                onChange={e => setForm(f => ({ ...f, is_emergency_referral: e.target.checked }))}
                style={{ width: '16px', height: '16px', cursor: 'pointer' }}
              />
              <label htmlFor="emergency-ref" style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                Mark as Emergency Referral (requires immediate veterinary attention on site)
              </label>
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', paddingTop: '8px', borderTop: '1px solid var(--border-subtle)' }}>
              <button
                type="submit"
                className="btn btn-primary"
                id="submit-response"
                disabled={submitting}
              >
                {submitting ? 'Submitting…' : '✓ Submit Response'}
              </button>
            </div>
          </form>
        </div>
      ) : null}
    </div>
  );
}

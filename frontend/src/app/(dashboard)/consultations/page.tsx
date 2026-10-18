'use client';

import { useEffect, useState, useCallback } from 'react';
import Link from 'next/link';
import { Search, Filter, ArrowRight } from 'lucide-react';
import apiClient from '@/lib/api-client';
import type { ConsultationListResponse } from '@/types/consultation';
import { formatRelativeTime, statusLabel, priorityLabel } from '@/lib/utils';

const STATUSES = ['', 'pending', 'in_progress', 'responded', 'overdue', 'closed'];
const PRIORITIES = ['', 'normal', 'urgent', 'emergency'];

export default function ConsultationsPage() {
  const [data, setData]       = useState<ConsultationListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage]       = useState(1);
  const [status, setStatus]   = useState('');
  const [priority, setPriority] = useState('');
  const [search, setSearch]   = useState('');
  const [searchInput, setSearchInput] = useState('');

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page: String(page), page_size: '15' });
      if (status)   params.set('status',   status);
      if (priority) params.set('priority', priority);
      if (search)   params.set('search',   search);
      const r = await apiClient.get<ConsultationListResponse>(`/consultations?${params}`);
      setData(r.data);
    } finally {
      setLoading(false);
    }
  }, [page, status, priority, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setSearch(searchInput);
    setPage(1);
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Filters bar */}
      <div className="card" style={{ padding: '16px 20px' }}>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
          <form onSubmit={handleSearch} style={{ flex: '1 1 220px', display: 'flex', gap: '8px' }}>
            <div style={{ position: 'relative', flex: 1 }}>
              <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                className="form-input"
                style={{ paddingLeft: '36px' }}
                placeholder="Search cases, animals, workers…"
                value={searchInput}
                onChange={e => setSearchInput(e.target.value)}
              />
            </div>
            <button className="btn btn-primary" type="submit" style={{ padding: '10px 16px' }}>
              <Search size={15} />
            </button>
          </form>

          <select className="form-select" style={{ flex: '0 1 160px' }} value={status} onChange={e => { setStatus(e.target.value); setPage(1); }}>
            {STATUSES.map(s => <option key={s} value={s}>{s ? statusLabel(s) : 'All Statuses'}</option>)}
          </select>

          <select className="form-select" style={{ flex: '0 1 160px' }} value={priority} onChange={e => { setPriority(e.target.value); setPage(1); }}>
            {PRIORITIES.map(p => <option key={p} value={p}>{p ? priorityLabel(p) : 'All Priorities'}</option>)}
          </select>
        </div>
      </div>

      {/* Results */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        {/* Header */}
        <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ fontSize: '0.875rem', fontWeight: 600 }}>
            {data ? `${data.total} consultation${data.total !== 1 ? 's' : ''}` : 'Loading…'}
          </h3>
        </div>

        {loading ? (
          <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {Array.from({ length: 6 }).map((_, i) => <div key={i} className="skeleton" style={{ height: '56px' }} />)}
          </div>
        ) : data?.items.length === 0 ? (
          <div className="empty-state">
            <Search size={48} />
            <p>No consultations match your filters.</p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Reference</th>
                <th>Animal / Owner</th>
                <th>Zone</th>
                <th>Field Worker</th>
                <th>Priority</th>
                <th>Status</th>
                <th>SLA</th>
                <th>Submitted</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {data?.items.map((c, i) => (
                <tr key={c.id}>
                  <td>
                    <span style={{ fontFamily: 'monospace', fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                      {c.aisp_reference ?? `#${c.id}`}
                    </span>
                  </td>
                  <td>
                    <div style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{c.animal_species}{c.animal_breed ? ` · ${c.animal_breed}` : ''}</div>
                  </td>
                  <td style={{ fontSize: '0.8125rem' }}>{c.zone_name ?? '—'}</td>
                  <td style={{ fontSize: '0.8125rem' }}>{c.field_worker_name}</td>
                  <td><span className={`badge badge-${c.priority}`}>{priorityLabel(c.priority)}</span></td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <div className={`status-dot ${c.status}`} />
                      <span style={{ fontSize: '0.8125rem' }}>{statusLabel(c.status)}</span>
                    </div>
                  </td>
                  <td style={{ fontSize: '0.75rem', color: c.sla_deadline && new Date(c.sla_deadline) < new Date() ? 'var(--status-overdue)' : 'var(--text-muted)' }}>
                    {c.sla_deadline ? formatRelativeTime(c.sla_deadline) : '—'}
                  </td>
                  <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{formatRelativeTime(c.submitted_at)}</td>
                  <td>
                    <Link href={`/consultations/${c.id}`} className="btn btn-ghost" style={{ padding: '6px 12px', fontSize: '0.8125rem' }}>
                      Open <ArrowRight size={12} />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div style={{ padding: '16px 20px', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'center', gap: '8px' }}>
            <button className="btn btn-secondary" disabled={page === 1} onClick={() => setPage(p => p - 1)} style={{ padding: '6px 14px' }}>
              Previous
            </button>
            <span style={{ display: 'flex', alignItems: 'center', fontSize: '0.875rem', color: 'var(--text-muted)', padding: '0 8px' }}>
              Page {page} of {data.total_pages}
            </span>
            <button className="btn btn-secondary" disabled={page === data.total_pages} onClick={() => setPage(p => p + 1)} style={{ padding: '6px 14px' }}>
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

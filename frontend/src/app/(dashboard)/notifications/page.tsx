'use client';

import { useEffect, useState } from 'react';
import { Bell, CheckCheck, AlertTriangle, Info, Zap, Stethoscope } from 'lucide-react';
import Link from 'next/link';
import apiClient from '@/lib/api-client';
import type { NotificationListResponse, Notification } from '@/types/api';
import { formatRelativeTime } from '@/lib/utils';

const typeConfig: Record<string, { icon: React.ElementType; color: string; bg: string }> = {
  info:      { icon: Info,          color: 'hsl(213,91%,60%)', bg: 'hsl(213,91%,8%)' },
  warning:   { icon: AlertTriangle, color: 'hsl(43,96%,56%)',  bg: 'hsl(43,96%,8%)'  },
  overdue:   { icon: AlertTriangle, color: 'hsl(0,84%,60%)',   bg: 'hsl(0,84%,8%)'   },
  new_case:  { icon: Stethoscope,   color: 'hsl(142,70%,50%)', bg: 'hsl(142,70%,6%)' },
  emergency: { icon: Zap,           color: 'hsl(0,84%,60%)',   bg: 'hsl(0,84%,8%)'   },
};

function NotificationItem({ notification, onMarkRead }: { notification: Notification; onMarkRead: (id: number) => void }) {
  const cfg = typeConfig[notification.notification_type] ?? typeConfig.info;
  const Icon = cfg.icon;

  return (
    <div style={{
      display: 'flex', gap: '14px', alignItems: 'flex-start',
      padding: '16px 20px',
      background: notification.is_read ? 'transparent' : 'rgba(59,130,246,0.04)',
      borderBottom: '1px solid var(--border-subtle)',
      transition: 'background 0.2s',
      opacity: notification.is_read ? 0.7 : 1,
    }}>
      <div style={{
        width: '36px', height: '36px', borderRadius: 'var(--radius-md)',
        background: cfg.bg, color: cfg.color,
        display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
      }}>
        <Icon size={16} />
      </div>

      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
          <span style={{ fontWeight: 600, fontSize: '0.875rem', color: 'var(--text-primary)' }}>
            {notification.title}
          </span>
          {!notification.is_read && (
            <span style={{ width: '7px', height: '7px', borderRadius: '50%', background: 'var(--brand-500)', flexShrink: 0 }} />
          )}
        </div>
        <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '8px' }}>
          {notification.body}
        </p>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {formatRelativeTime(notification.created_at)}
          </span>
          {notification.consultation_id && (
            <Link
              href={`/consultations/${notification.consultation_id}`}
              style={{ fontSize: '0.75rem', color: 'var(--brand-400)', fontWeight: 500 }}
            >
              View case →
            </Link>
          )}
          {!notification.is_read && (
            <button
              onClick={() => onMarkRead(notification.id)}
              style={{ fontSize: '0.75rem', color: 'var(--text-muted)', background: 'none', border: 'none', cursor: 'pointer' }}
            >
              Mark read
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default function NotificationsPage() {
  const [data, setData]       = useState<NotificationListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [unreadOnly, setUnreadOnly] = useState(false);

  async function load() {
    setLoading(true);
    try {
      const r = await apiClient.get<NotificationListResponse>(`/notifications?unread_only=${unreadOnly}`);
      setData(r.data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, [unreadOnly]);

  async function markRead(id: number) {
    await apiClient.patch(`/notifications/${id}/read`);
    setData(prev => prev ? {
      ...prev,
      items: prev.items.map(n => n.id === id ? { ...n, is_read: true } : n),
      unread_count: Math.max(0, prev.unread_count - 1),
    } : prev);
  }

  async function markAllRead() {
    const unread = data?.items.filter(n => !n.is_read) ?? [];
    await Promise.all(unread.map(n => apiClient.patch(`/notifications/${n.id}/read`)));
    setData(prev => prev ? {
      ...prev,
      items: prev.items.map(n => ({ ...n, is_read: true })),
      unread_count: 0,
    } : prev);
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ marginBottom: '4px' }}>Notifications</h1>
          {data && (
            <p>{data.unread_count > 0 ? `${data.unread_count} unread` : 'All caught up!'}</p>
          )}
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            className={`btn ${unreadOnly ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setUnreadOnly(v => !v)}
            style={{ padding: '8px 16px', fontSize: '0.8125rem' }}
          >
            {unreadOnly ? '● Unread only' : 'Show all'}
          </button>
          {(data?.unread_count ?? 0) > 0 && (
            <button className="btn btn-ghost" onClick={markAllRead} style={{ padding: '8px 16px', fontSize: '0.8125rem' }}>
              <CheckCheck size={15} /> Mark all read
            </button>
          )}
        </div>
      </div>

      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        {loading ? (
          <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {Array.from({ length: 4 }).map((_, i) => <div key={i} className="skeleton" style={{ height: '72px' }} />)}
          </div>
        ) : !data?.items.length ? (
          <div className="empty-state">
            <Bell size={48} />
            <p>{unreadOnly ? 'No unread notifications.' : 'No notifications yet.'}</p>
          </div>
        ) : (
          data.items.map(n => (
            <NotificationItem key={n.id} notification={n} onMarkRead={markRead} />
          ))
        )}
      </div>
    </div>
  );
}

'use client';

import { Bell, Search } from 'lucide-react';
import { useState, useEffect } from 'react';
import apiClient from '@/lib/api-client';
import type { NotificationListResponse } from '@/types/api';

interface TopbarProps {
  title: string;
}

export default function Topbar({ title }: TopbarProps) {
  const [unread, setUnread] = useState(0);

  useEffect(() => {
    apiClient.get<NotificationListResponse>('/notifications')
      .then(r => setUnread(r.data.unread_count))
      .catch(() => {});
  }, []);

  return (
    <header className="topbar">
      <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)' }}>
        {title}
      </h2>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <button className="btn btn-ghost" style={{ padding: '8px', borderRadius: 'var(--radius-md)', position: 'relative' }}>
          <Bell size={18} />
          {unread > 0 && (
            <span style={{
              position: 'absolute', top: '4px', right: '4px',
              width: '16px', height: '16px', borderRadius: '50%',
              background: 'var(--status-overdue)',
              fontSize: '0.625rem', fontWeight: 700,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: '#fff',
            }}>
              {unread > 9 ? '9+' : unread}
            </span>
          )}
        </button>
      </div>
    </header>
  );
}

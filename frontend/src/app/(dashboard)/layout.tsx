'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getStoredUser, isAuthenticated, logout } from '@/lib/auth';
import type { CurrentUser } from '@/types/api';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace('/login');
      return;
    }
    setUser(getStoredUser());
  }, [router]);

  return (
    <div style={{ minHeight: '100dvh' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 16, padding: '15px max(24px, calc((100% - 1080px) / 2))', borderBottom: '1px solid var(--border-subtle)' }}>
        <a href="/dashboard" style={{ color: 'var(--text-primary)', fontWeight: 700, textDecoration: 'none' }}>CareConnect</a>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          {user && <span style={{ color: 'var(--text-secondary)', fontSize: 14 }}>{user.full_name} · {user.role}</span>}
          <button className="btn btn-ghost" onClick={logout}>Sign out</button>
        </div>
      </header>
      <main style={{ padding: '36px 24px 64px' }}>{children}</main>
    </div>
  );
}

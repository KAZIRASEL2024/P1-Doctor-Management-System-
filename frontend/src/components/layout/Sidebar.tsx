'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard, Stethoscope, Users, MapPin,
  Bell, Settings, LogOut, Activity, PawPrint
} from 'lucide-react';
import { logout, getStoredUser } from '@/lib/auth';
import type { CurrentUser } from '@/types/api';

const navItems = [
  { href: '/dashboard',     label: 'Dashboard',      icon: LayoutDashboard },
  { href: '/consultations', label: 'Consultations',  icon: Stethoscope },
  { href: '/doctors',       label: 'Doctors',        icon: Users },
  { href: '/patients',      label: 'Patients',       icon: PawPrint },
  { href: '/zones',         label: 'Zones',          icon: MapPin },
  { href: '/notifications', label: 'Notifications',  icon: Bell },
  { href: '/settings',      label: 'Settings',       icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const initials = user?.full_name
    .split(' ')
    .slice(0, 2)
    .map(p => p[0])
    .join('')
    .toUpperCase() ?? 'U';

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '38px', height: '38px', borderRadius: '10px',
            background: 'linear-gradient(135deg, var(--brand-500), var(--brand-700))',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 4px 12px rgba(59,130,246,0.3)',
            flexShrink: 0,
          }}>
            <Activity size={18} color="white" />
          </div>
          <div>
            <div style={{ fontSize: '0.875rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.2 }}>
              BRAC AISP
            </div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
              Doctor Portal
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        {navItems.map(({ href, label, icon: Icon }) => {
          const isActive = pathname === href || pathname.startsWith(href + '/');
          return (
            <Link key={href} href={href} className={`nav-item ${isActive ? 'active' : ''}`}>
              <Icon className="nav-icon" size={18} />
              <span>{label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer / User */}
      <div className="sidebar-footer">
        {user && (
          <div style={{
            padding: '12px',
            background: 'var(--bg-elevated)',
            borderRadius: 'var(--radius-md)',
            marginBottom: '8px',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div className="avatar-placeholder" style={{ width: '36px', height: '36px', fontSize: '0.75rem' }}>
                {initials}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user.full_name}
                </div>
                <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'capitalize' }}>
                  {user.role}
                </div>
              </div>
            </div>
          </div>
        )}
        <button className="nav-item" style={{ width: '100%', background: 'none', border: 'none' }} onClick={() => logout()}>
          <LogOut size={18} className="nav-icon" />
          <span>Sign out</span>
        </button>
      </div>
    </aside>
  );
}

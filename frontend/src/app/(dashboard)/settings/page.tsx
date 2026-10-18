'use client';

import { useEffect, useState } from 'react';
import { getStoredUser } from '@/lib/auth';
import type { CurrentUser } from '@/types/api';
import { User, Shield, Info, Database, Globe } from 'lucide-react';

export default function SettingsPage() {
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => { setUser(getStoredUser()); }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '680px' }}>
      <div>
        <h1 style={{ marginBottom: '4px' }}>Settings</h1>
        <p>System configuration and account information.</p>
      </div>

      {/* Account info */}
      <div className="card">
        <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <User size={18} /> Account Information
        </h3>
        {user && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {[
              { label: 'Full Name', value: user.full_name },
              { label: 'Email', value: user.email },
              { label: 'Role', value: user.role.charAt(0).toUpperCase() + user.role.slice(1) },
              { label: 'Status', value: user.is_active ? 'Active' : 'Inactive' },
            ].map(({ label, value }) => (
              <div key={label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontWeight: 500 }}>{label}</span>
                <span style={{ fontSize: '0.875rem', color: 'var(--text-primary)' }}>{value}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* System info */}
      <div className="card">
        <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Database size={18} /> System Information
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
          {[
            { label: 'Application',   value: 'BRAC AISP Doctor Management System' },
            { label: 'Version',       value: '1.0.0' },
            { label: 'Backend URL',   value: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000' },
            { label: 'API Docs',      value: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/docs` },
            { label: 'Environment',   value: process.env.NODE_ENV || 'development' },
          ].map(({ label, value }) => (
            <div key={label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontWeight: 500 }}>{label}</span>
              <span style={{ fontSize: '0.8125rem', color: 'var(--text-primary)', fontFamily: 'monospace' }}>{value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Integration status */}
      <div className="card">
        <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Globe size={18} /> Integration Status
        </h3>
        <div className="alert alert-warning" style={{ marginBottom: '16px' }}>
          <Info size={15} />
          External integrations are not yet active. This is the demo configuration.
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {[
            { label: 'AISP Mobile API',     status: 'Not Configured', color: 'var(--status-pending)' },
            { label: 'BRAC ERP System',      status: 'Not Configured', color: 'var(--status-pending)' },
            { label: 'Object Storage (S3)',  status: 'Demo Mode',      color: 'hsl(43,96%,56%)'       },
            { label: 'PostgreSQL Database',  status: 'Connected',      color: 'var(--status-responded)' },
          ].map(({ label, status, color }) => (
            <div key={label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{label}</span>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color }}>{status}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Security */}
      <div className="card">
        <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Shield size={18} /> Security & Permissions
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          <div style={{ display: 'flex', gap: '10px', padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
            <span style={{ color: 'var(--status-responded)' }}>✓</span>
            JWT-based authentication with configurable token expiry
          </div>
          <div style={{ display: 'flex', gap: '10px', padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
            <span style={{ color: 'var(--status-responded)' }}>✓</span>
            Role-based access control (Admin / Doctor)
          </div>
          <div style={{ display: 'flex', gap: '10px', padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
            <span style={{ color: 'var(--status-responded)' }}>✓</span>
            Zone-restricted access enforced on the backend
          </div>
          <div style={{ display: 'flex', gap: '10px', padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
            <span style={{ color: 'var(--status-responded)' }}>✓</span>
            bcrypt password hashing
          </div>
          <div style={{ display: 'flex', gap: '10px', padding: '10px 0' }}>
            <span style={{ color: 'hsl(43,96%,56%)' }}>⚠</span>
            2FA and audit log viewing — planned for future release
          </div>
        </div>
      </div>
    </div>
  );
}

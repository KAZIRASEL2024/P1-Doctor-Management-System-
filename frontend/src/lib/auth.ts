/**
 * Auth utilities for login/logout and token management.
 */
import apiClient from './api-client';
import type { CurrentUser, TokenResponse } from '@/types/api';

export async function login(email: string, password: string): Promise<CurrentUser> {
  const { data } = await apiClient.post<TokenResponse>('/auth/login', { email, password });
  localStorage.setItem('dms_token', data.access_token);

  const { data: user } = await apiClient.get<CurrentUser>('/auth/me');
  localStorage.setItem('dms_user', JSON.stringify(user));
  return user;
}

export function logout(): void {
  localStorage.removeItem('dms_token');
  localStorage.removeItem('dms_user');
  window.location.href = '/login';
}

export function getStoredUser(): CurrentUser | null {
  if (typeof window === 'undefined') return null;
  const raw = localStorage.getItem('dms_user');
  if (!raw) return null;
  try {
    return JSON.parse(raw) as CurrentUser;
  } catch {
    return null;
  }
}

export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false;
  return !!localStorage.getItem('dms_token');
}

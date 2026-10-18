'use client';

import { useState, useEffect, useCallback } from 'react';
import { login as loginFn, logout as logoutFn, getStoredUser, isAuthenticated } from '@/lib/auth';
import type { CurrentUser } from '@/types/api';

export function useAuth() {
  const [user, setUser]           = useState<CurrentUser | null>(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState<string | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const stored = getStoredUser();
    if (stored) {
      setUser(stored);
      setIsLoggedIn(true);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const u = await loginFn(email, password);
      setUser(u);
      setIsLoggedIn(true);
      return u;
    } catch (err: any) {
      const msg = err.response?.data?.error ?? 'Invalid credentials.';
      setError(msg);
      throw new Error(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    logoutFn();
    setUser(null);
    setIsLoggedIn(false);
  }, []);

  return { user, loading, error, isLoggedIn, login, logout };
}

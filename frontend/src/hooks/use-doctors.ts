'use client';

import { useState, useEffect, useCallback } from 'react';
import apiClient from '@/lib/api-client';
import type { DoctorListResponse, Doctor } from '@/types/doctor';

export function useDoctors() {
  const [data, setData]       = useState<DoctorListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);

  useEffect(() => {
    apiClient.get<DoctorListResponse>('/doctors')
      .then(r => setData(r.data))
      .catch(err => setError(err.response?.data?.error ?? 'Failed to load doctors.'))
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}

export function useDoctorDetail(id: string | number) {
  const [data, setData]       = useState<Doctor | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);

  useEffect(() => {
    apiClient.get<Doctor>(`/doctors/${id}`)
      .then(r => setData(r.data))
      .catch(err => setError(err.response?.data?.error ?? 'Doctor not found.'))
      .finally(() => setLoading(false));
  }, [id]);

  return { data, loading, error };
}

'use client';

import { useState, useEffect, useCallback } from 'react';
import apiClient from '@/lib/api-client';
import type { ConsultationListResponse, ConsultationDetail } from '@/types/consultation';

interface UseConsultationsOptions {
  page?: number;
  pageSize?: number;
  status?: string;
  priority?: string;
  zoneId?: number;
  search?: string;
}

export function useConsultations(options: UseConsultationsOptions = {}) {
  const { page = 1, pageSize = 20, status, priority, zoneId, search } = options;
  const [data, setData]       = useState<ConsultationListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ page: String(page), page_size: String(pageSize) });
      if (status)  params.set('status',   status);
      if (priority) params.set('priority', priority);
      if (zoneId)  params.set('zone_id',  String(zoneId));
      if (search)  params.set('search',   search);
      const r = await apiClient.get<ConsultationListResponse>(`/consultations?${params}`);
      setData(r.data);
    } catch (err: any) {
      setError(err.response?.data?.error ?? 'Failed to load consultations.');
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, status, priority, zoneId, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

export function useConsultationDetail(id: string | number) {
  const [data, setData]       = useState<ConsultationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await apiClient.get<ConsultationDetail>(`/consultations/${id}`);
      setData(r.data);
    } catch (err: any) {
      setError(err.response?.data?.error ?? 'Consultation not found.');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

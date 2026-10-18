import { type ClassValue, clsx } from 'clsx';
import { formatDistanceToNow, format, isPast } from 'date-fns';
import axios from 'axios';

export function cn(...inputs: ClassValue[]): string {
  return clsx(inputs);
}

export function formatRelativeTime(dateStr: string): string {
  return formatDistanceToNow(new Date(dateStr), { addSuffix: true });
}

export function formatDate(dateStr: string, fmt = 'dd MMM yyyy, HH:mm'): string {
  return format(new Date(dateStr), fmt);
}

export function isOverdue(slaDeadline: string | null): boolean {
  if (!slaDeadline) return false;
  return isPast(new Date(slaDeadline));
}

export function priorityLabel(p: string): string {
  return { normal: 'Normal', urgent: 'Urgent', emergency: 'Emergency' }[p] ?? p;
}

export function statusLabel(s: string): string {
  return {
    pending: 'Pending',
    in_progress: 'In Progress',
    responded: 'Responded',
    closed: 'Closed',
    overdue: 'Overdue',
  }[s] ?? s;
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function getApiErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError<{ error?: string; detail?: string }>(error)) {
    return error.response?.data?.error ?? error.response?.data?.detail ?? fallback;
  }
  return fallback;
}

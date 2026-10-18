// API response types

export interface DashboardStats {
  total_consultations: number;
  pending_consultations: number;
  in_progress_consultations: number;
  responded_consultations: number;
  overdue_consultations: number;
  total_doctors: number;
  active_zones: number;
  avg_response_time_minutes: number | null;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  role: string;
}

export interface CurrentUser {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

export interface Notification {
  id: number;
  consultation_id: number | null;
  title: string;
  body: string;
  notification_type: string;
  is_read: boolean;
  created_at: string;
}

export interface NotificationListResponse {
  items: Notification[];
  total: number;
  unread_count: number;
}

export interface ApiError {
  error: string;
  status_code: number;
}

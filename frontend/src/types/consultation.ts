// Consultation TypeScript types

export type ConsultationStatus = 'pending' | 'in_progress' | 'responded' | 'overdue' | 'closed';
export type ConsultationPriority = 'normal' | 'urgent' | 'emergency';
export type AttachmentType = 'photo' | 'audio' | 'document';

export interface Attachment {
  id: number;
  consultation_id: number;
  file_name: string;
  file_type: AttachmentType;
  mime_type: string;
  storage_path: string;
  file_size_bytes: number;
  uploaded_at: string;
}

export interface ConsultationResponse {
  id: number;
  consultation_id: number;
  doctor_id: number;
  diagnosis: string;
  treatment_plan: string;
  medications: string | null;
  follow_up_instructions: string | null;
  is_emergency_referral: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface ConsultationSummary {
  id: number;
  aisp_reference: string | null;
  zone_id: number | null;
  zone_name: string | null;
  field_worker_name: string;
  field_worker_phone: string | null;
  animal_species: string;
  animal_breed: string | null;
  priority: ConsultationPriority;
  status: ConsultationStatus;
  submitted_at: string;
  sla_deadline: string | null;
  response_count: number;
}

export interface ConsultationDetail extends ConsultationSummary {
  animal_age_months: number | null;
  animal_weight_kg: number | null;
  animal_temperature_celsius: number | null;
  animal_owner_name: string | null;
  symptoms: string;
  remarks: string | null;
  responded_at: string | null;
  closed_at: string | null;
  attachments: Attachment[];
  responses: ConsultationResponse[];
}

export interface ConsultationListResponse {
  items: ConsultationSummary[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ResponseSubmit {
  consultation_id: number;
  diagnosis: string;
  treatment_plan: string;
  medications?: string;
  follow_up_instructions?: string;
  is_emergency_referral?: boolean;
}

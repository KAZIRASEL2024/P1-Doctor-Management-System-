// Doctor TypeScript types

export interface DoctorZone {
  id: number;
  name: string;
}

export interface Doctor {
  id: number;
  user_id: number;
  full_name: string;
  email: string;
  registration_number: string;
  specialization: string;
  qualification: string;
  phone: string;
  bio: string | null;
  avatar_url: string | null;
  is_emergency_doctor: boolean;
  is_available: boolean;
  zones: DoctorZone[];
  total_responses: number;
}

export interface DoctorListResponse {
  items: Doctor[];
  total: number;
}

export interface DoctorCreate {
  full_name: string;
  email: string;
  password: string;
  registration_number: string;
  specialization: string;
  qualification: string;
  phone: string;
  bio?: string;
  is_emergency_doctor: boolean;
  is_available: boolean;
  zone_ids: number[];
}

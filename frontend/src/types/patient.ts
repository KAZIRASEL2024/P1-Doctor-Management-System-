export interface Patient {
  id: number;
  name: string;
  species: string;
  breed: string | null;
  sex: string | null;
  age_months: number | null;
  weight_kg: number | null;
  owner_name: string;
  owner_phone: string | null;
  location: string | null;
  medical_notes: string | null;
  created_at: string;
}

export interface PatientListResponse {
  items: Patient[];
  total: number;
}

export type PatientCreate = Omit<Patient, 'id' | 'created_at'>;

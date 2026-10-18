// Zone types

export interface Zone {
  id: number;
  name: string;
  erp_region_code: string | null;
  description: string | null;
  is_active: boolean;
  doctor_count: number;
  consultation_count: number;
}

export interface ZoneListResponse {
  items: Zone[];
  total: number;
}

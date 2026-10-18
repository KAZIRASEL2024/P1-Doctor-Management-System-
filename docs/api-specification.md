# API Specification

Base URL: `http://localhost:8000/api`

Interactive docs: `http://localhost:8000/api/docs` (Swagger UI)

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

---

## Auth

### POST /auth/login
Login with email and password.

**Request**
```json
{ "email": "admin@brac-aisp.org", "password": "Admin@1234" }
```
**Response 200**
```json
{ "access_token": "eyJ...", "token_type": "bearer", "expires_in": 3600 }
```

### GET /auth/me
Returns the current authenticated user.

---

## Dashboard

### GET /dashboard/stats
Returns consultation counts, doctor count, and active zones.

---

## Consultations

### GET /consultations
List consultations with optional filters.

Query params: `page`, `page_size`, `status`, `priority`, `zone_id`, `search`

### GET /consultations/{id}
Full consultation detail including attachments and responses.

---

## Responses

### POST /responses
Submit a doctor response. Updates consultation status to `responded`.

**Request**
```json
{
  "consultation_id": 1,
  "diagnosis": "Suspected respiratory infection...",
  "treatment_plan": "1. Isolate animal...",
  "medications": "Oxytetracycline 5mg/kg",
  "follow_up_instructions": "Recheck in 5 days",
  "is_emergency_referral": false
}
```

---

## Doctors

### POST /doctors — Create a doctor (admin only)
Creates a doctor account and profile. The request includes `full_name`, `email`, `password`, `registration_number`, `specialization`, `qualification`, and `phone`; `bio`, `is_emergency_doctor`, `is_available`, and `zone_ids` are optional.

### GET /doctors — List all doctors with zone assignments
### GET /doctors/{id} — Doctor profile detail

## Patients

### POST /patients — Create an animal patient profile
Requires `name`, `species`, and `owner_name`. Optional fields include breed, sex, age in months, weight, owner phone, location, and medical notes.

### GET /patients — List registered patients
### GET /patients/{id} — Patient profile detail

---

## Zones

### GET /zones — List all zones with doctor and case counts

---

## Notifications

### GET /notifications — List notifications (`?unread_only=true`)
### PATCH /notifications/{id}/read — Mark a notification as read

---

## Health

### GET /health — Returns `{"status":"ok"}` (no auth required)

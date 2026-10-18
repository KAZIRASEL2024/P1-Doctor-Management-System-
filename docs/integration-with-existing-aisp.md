# Integration Guide: Connecting the Existing AISP API

## Overview

The BRAC AISP mobile application and its backend form a separate, existing system.
This Doctor Management System (DMS) must **not** modify AISP data directly.
All communication goes through the adapter in `backend/app/integrations/aisp_client.py`.

## Integration Boundary

```
AISP Mobile App  ──→  AISP Backend (existing)
                              │
                    [AISP REST API — TBD]
                              │
                     aisp_client.py adapter
                              │
                    DMS Backend (this system)
                              │
                    DMS PostgreSQL database
```

## What This System Stores

| Field | Source | Notes |
|-------|--------|-------|
| `consultations.aisp_reference` | AISP | External ID — do not modify |
| `consultations.field_worker_name` | AISP | For display only |
| `consultations.symptoms`, vitals | AISP | Copied at import time |
| `consultation_responses.*` | DMS | Owned by this system |

## Steps to Connect

1. Obtain AISP API documentation (base URL, auth method, endpoints)
2. Implement `AISPClient.fetch_consultations()` in `aisp_client.py`
3. Implement `AISPClient.deliver_response()` to send doctor feedback back
4. Replace `seed_demo_data.py` usage in production with scheduled polling
5. Validate field mapping against the confirmed AISP schema
6. Write integration tests in `tests/test_routing.py`

## Data Flow (once integrated)

```
AISP Backend
    │  GET /consultations (polled every N minutes)
    ▼
aisp_client.fetch_consultations()
    │  map fields → Consultation model
    ▼
consultation_service.create_from_aisp()
    │  save to PostgreSQL
    ▼
Doctor dashboard shows new case
    │  Doctor submits response
    ▼
response_service.submit_response()
    │  save ConsultationResponse
    ▼
aisp_client.deliver_response()
    │  POST /responses to AISP
    ▼
AISP Backend notifies field worker
```

## ERP Region Code Alignment

BRAC ERP region codes are stored in `zones.erp_region_code`.
The `erp_client.py` adapter will sync zone metadata once the ERP API is available.
No production data should be written to ERP from this system without explicit authorization.

## Security Notes

- Store AISP API credentials in environment variables, never in code
- Use HTTPS for all external API calls
- Log all AISP API calls to the audit_logs table
- Rate-limit polling to avoid overwhelming the AISP backend

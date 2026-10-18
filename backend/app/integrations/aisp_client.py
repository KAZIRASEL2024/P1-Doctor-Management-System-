"""
AISP Client — integration adapter for the BRAC AISP mobile backend.

STATUS: NOT IMPLEMENTED
This is a stub that documents the expected interface.
Implement the methods here when the AISP API documentation is available.
Do NOT modify AISP data directly — only read consultations and deliver responses.

See docs/integration-with-existing-aisp.md for the full integration plan.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class AISPConsultation:
    """Represents a consultation fetched from the AISP backend."""
    aisp_reference: str
    field_worker_name: str
    field_worker_phone: str | None
    zone_erp_code: str | None
    animal_species: str
    animal_breed: str | None
    symptoms: str
    priority: str
    submitted_at: str  # ISO 8601


class AISPClient:
    """
    Adapter for the BRAC AISP REST API.

    All methods raise NotImplementedError until the API contract is confirmed.
    This keeps the integration boundary explicit and prevents accidental calls
    to a non-existent endpoint.
    """

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key  = api_key

    async def fetch_consultations(self, since_timestamp: str | None = None) -> List[AISPConsultation]:
        """
        Fetch new consultations from the AISP backend since a given timestamp.

        TODO: Implement when AISP API documentation is available.
        Expected endpoint: GET /consultations?since=<ISO8601>
        """
        raise NotImplementedError(
            "AISP API integration is not yet configured. "
            "See docs/integration-with-existing-aisp.md."
        )

    async def deliver_response(self, aisp_reference: str, response_payload: dict) -> bool:
        """
        Deliver a doctor's response back to the AISP backend.

        TODO: Implement when AISP API documentation is available.
        Expected endpoint: POST /responses/{aisp_reference}
        Returns True if delivery succeeded.
        """
        raise NotImplementedError(
            "AISP API integration is not yet configured. "
            "See docs/integration-with-existing-aisp.md."
        )

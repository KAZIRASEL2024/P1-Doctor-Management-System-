"""
ERP Client — adapter for BRAC ERP region code synchronisation.

STATUS: NOT IMPLEMENTED
Implement when ERP API details are available.
"""
from __future__ import annotations


class ERPClient:
    """Stub for BRAC ERP system integration."""

    def __init__(self, base_url: str, credentials: dict) -> None:
        self.base_url    = base_url
        self.credentials = credentials

    async def sync_zone_metadata(self) -> None:
        """
        Fetch region codes from ERP and update zones.erp_region_code.

        TODO: Implement when ERP API is available.
        """
        raise NotImplementedError("ERP integration is not yet configured.")

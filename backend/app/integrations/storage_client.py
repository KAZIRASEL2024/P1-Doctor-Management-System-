"""
Storage Client — abstraction for file storage (photos and audio from field workers).

STATUS: DEMO MODE
In demo mode, file references are stored in the database but files are not
served. In production, connect this to an S3-compatible object store.
"""
from __future__ import annotations

import os
from pathlib import Path


class StorageClient:
    """
    File storage abstraction.

    Demo implementation: files are stored on the local filesystem under
    STORAGE_ROOT (default: ./uploads).
    Production: replace with boto3 / S3-compatible client.
    """

    def __init__(self, storage_root: str | None = None) -> None:
        self.storage_root = Path(storage_root or os.getenv("STORAGE_ROOT", "./uploads"))
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def get_url(self, storage_path: str) -> str:
        """Return a URL for the stored file. Demo returns the path string."""
        # TODO: In production, generate a presigned S3 URL
        return f"/demo/files/{storage_path.lstrip('/')}"

    async def store(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        """
        Store a file and return its storage_path.

        TODO: Replace with S3 PUT when object storage is configured.
        """
        dest = self.storage_root / filename
        dest.write_bytes(file_bytes)
        return str(dest)

    async def delete(self, storage_path: str) -> None:
        """Delete a stored file."""
        path = Path(storage_path)
        if path.exists():
            path.unlink()

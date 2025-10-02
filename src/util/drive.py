"""Placeholder Google Drive adapter."""
from __future__ import annotations

from pathlib import Path
from typing import BinaryIO


class DriveClient:
    """Stub client that will handle Google Drive uploads/downloads."""

    def __init__(self) -> None:
        # TODO: implement OAuth device flow and Drive API interactions
        raise NotImplementedError("DriveClient is not implemented yet.")

    def upload(self, local_path: Path, remote_folder: str) -> str:
        raise NotImplementedError

    def download(self, file_id: str, destination: Path) -> None:
        raise NotImplementedError

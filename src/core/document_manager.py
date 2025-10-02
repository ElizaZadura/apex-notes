"""Manage lifecycle of open documents and file interactions."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional

from .document import Document


class DocumentManager:
    """Simple document registry handling open buffers and persistence."""

    def __init__(self) -> None:
        self._documents: Dict[int, Document] = {}
        self._counter = 0

    def create_document(self, text: str = "", path: Optional[Path] = None, *, encoding: str = "utf-8") -> int:
        document = Document(path=path, text=text, encoding=encoding)
        document_id = self._counter
        self._documents[document_id] = document
        self._counter += 1
        return document_id

    def close_document(self, document_id: int) -> None:
        self._documents.pop(document_id, None)

    def get_document(self, document_id: int) -> Document:
        return self._documents[document_id]

    def list_documents(self) -> Iterable[tuple[int, Document]]:
        return self._documents.items()

    def load_from_disk(self, file_path: Path, *, encoding: str = "utf-8") -> int:
        data = file_path.read_text(encoding=encoding)
        doc_id = self.create_document(text=data, path=file_path, encoding=encoding)
        document = self.get_document(doc_id)
        document.mark_clean()
        return doc_id

    def save_to_disk(self, document_id: int, file_path: Optional[Path] = None, *, encoding: Optional[str] = None) -> None:
        document = self.get_document(document_id)
        target_path = file_path or document.path
        if target_path is None:
            raise ValueError("No file path provided for document save operation.")
        target_path.write_text(document.text, encoding=encoding or document.encoding)
        document.path = target_path
        document.encoding = encoding or document.encoding
        document.mark_clean()

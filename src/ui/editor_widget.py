"""Qt editor widget wired to Document instances."""
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPlainTextEdit

from src.core.document import Document


class EditorWidget(QPlainTextEdit):
    """Simple plain-text editor bound to a document."""

    content_modified = Signal()

    def __init__(self, document: Document, parent=None) -> None:
        super().__init__(parent)
        self._document = document
        self._is_syncing = False
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))
        self.setPlainText(document.text)
        self.textChanged.connect(self._on_text_changed)

    @property
    def document(self) -> Document:
        return self._document

    def _on_text_changed(self) -> None:
        if self._is_syncing:
            return
        self._is_syncing = True
        try:
            self._document.text = self.toPlainText()
            self._document.mark_dirty()
        finally:
            self._is_syncing = False
        self.content_modified.emit()

    def reload_document(self) -> None:
        self._is_syncing = True
        try:
            self.setPlainText(self._document.text)
        finally:
            self._is_syncing = False

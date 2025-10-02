"""Document model representing an open text buffer."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Document:
    """Holds metadata and content for an open document."""

    path: Optional[Path]
    text: str = ""
    encoding: str = "utf-8"
    is_dirty: bool = False
    language: Optional[str] = None
    _undo_stack: list[str] = field(default_factory=list, init=False, repr=False)
    _redo_stack: list[str] = field(default_factory=list, init=False, repr=False)

    def mark_dirty(self) -> None:
        self.is_dirty = True

    def mark_clean(self) -> None:
        self.is_dirty = False

    def set_text(self, text: str) -> None:
        self.text = text
        self.mark_dirty()

    def snapshot(self) -> str:
        """Return the current buffer snapshot."""
        return self.text

    def display_name(self) -> str:
        if self.path is None:
            return "Untitled"
        return self.path.name

"""Utility for loading and resolving key bindings."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import json


DEFAULT_KEYMAP = {
    "file.new": "Ctrl+N",
    "file.open": "Ctrl+O",
    "file.save": "Ctrl+S",
    "view.split_horizontal": "Ctrl+Shift+S",
    "macro.start_recording": "Ctrl+Alt+R",
    "macro.stop_recording": "Ctrl+Alt+Shift+R",
    "macro.play": "Ctrl+Alt+P",
}


@dataclass(frozen=True)
class KeyBinding:
    command: str
    shortcut: str


class Keymap:
    """Resolve command identifiers to shortcuts with override support."""

    def __init__(self, overrides: Dict[str, str] | None = None) -> None:
        mapping = DEFAULT_KEYMAP.copy()
        if overrides:
            mapping.update(overrides)
        self._bindings = {command: KeyBinding(command, shortcut) for command, shortcut in mapping.items()}

    def binding_for(self, command: str) -> KeyBinding | None:
        return self._bindings.get(command)

    @classmethod
    def from_file(cls, path: Path) -> "Keymap":
        data = json.loads(path.read_text(encoding="utf-8"))
        overrides = {str(k): str(v) for k, v in data.items()}
        return cls(overrides=overrides)

"""Macro recording and playback primitives."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List


Command = Callable[[], None]


@dataclass
class Macro:
    name: str
    commands: List[str]


class MacroEngine:
    """Tracks macro recordings as sequences of command identifiers."""

    def __init__(self) -> None:
        self._macros: Dict[str, Macro] = {}
        self._recording: List[str] | None = None
        self._registry: Dict[str, Command] = {}

    def register_command(self, name: str, command: Command) -> None:
        self._registry[name] = command

    def start_recording(self) -> None:
        self._recording = []

    def stop_recording(self, name: str) -> None:
        if self._recording is None:
            return
        self._macros[name] = Macro(name=name, commands=list(self._recording))
        self._recording = None

    def record(self, command_name: str) -> None:
        if self._recording is not None:
            self._recording.append(command_name)

    def play(self, name: str) -> None:
        macro = self._macros.get(name)
        if not macro:
            return
        for command_name in macro.commands:
            command = self._registry.get(command_name)
            if command:
                command()

    def list_macros(self) -> List[str]:
        return list(self._macros.keys())

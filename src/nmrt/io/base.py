from __future__ import annotations

from pathlib import Path
from typing import Protocol

from nmrt.core.model import Recording


class RecordingReader(Protocol):
    name: str

    def can_read(self, path: str | Path) -> bool: ...
    def read(self, path: str | Path, **kwargs) -> Recording: ...


class RecordingWriter(Protocol):
    name: str

    def write(self, recording: Recording, path: str | Path, **kwargs) -> None: ...

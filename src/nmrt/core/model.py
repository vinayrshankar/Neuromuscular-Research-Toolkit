from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any

import numpy as np


@dataclass(frozen=True)
class Event:
    name: str
    time_s: float
    duration_s: float = 0.0
    value: str | float | int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Signal:
    name: str
    data: np.ndarray
    fs: float
    unit: str = "a.u."
    start_time_s: float = 0.0
    signal_type: str = "generic"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        arr = np.asarray(self.data, dtype=float).squeeze()
        if arr.ndim != 1:
            raise ValueError("Signal.data must be one-dimensional")
        if self.fs <= 0:
            raise ValueError("Signal.fs must be > 0")
        object.__setattr__(self, "data", arr)

    @property
    def n_samples(self) -> int:
        return int(self.data.size)

    @property
    def duration_s(self) -> float:
        return self.n_samples / self.fs

    @property
    def time_s(self) -> np.ndarray:
        return self.start_time_s + np.arange(self.n_samples) / self.fs

    def derived(self, data: np.ndarray, *, name: str | None = None, unit: str | None = None,
                signal_type: str | None = None, metadata: dict[str, Any] | None = None) -> Signal:
        merged = dict(self.metadata)
        if metadata:
            merged.update(metadata)
        return replace(
            self,
            name=name or self.name,
            data=np.asarray(data, dtype=float),
            unit=unit or self.unit,
            signal_type=signal_type or self.signal_type,
            metadata=merged,
        )


@dataclass
class Recording:
    signals: dict[str, Signal] = field(default_factory=dict)
    events: list[Event] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def add_signal(self, signal: Signal, overwrite: bool = False) -> None:
        if signal.name in self.signals and not overwrite:
            raise KeyError(f"Signal already exists: {signal.name}")
        self.signals[signal.name] = signal

    def add_event(self, event: Event) -> None:
        self.events.append(event)
        self.events.sort(key=lambda e: e.time_s)

    def record_step(self, name: str, **parameters: Any) -> None:
        self.history.append(
            {
                "step": name,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "parameters": parameters,
            }
        )

    def require(self, *names: str) -> tuple[Signal, ...]:
        missing = [n for n in names if n not in self.signals]
        if missing:
            raise KeyError(f"Missing required signals: {', '.join(missing)}")
        return tuple(self.signals[n] for n in names)

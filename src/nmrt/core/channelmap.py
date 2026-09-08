from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .model import Recording, Signal


@dataclass(frozen=True)
class ChannelRule:
    source: str
    name: str
    signal_type: str = "generic"
    unit: str = "a.u."
    scale: float = 1.0
    offset: float = 0.0
    invert: bool = False
    metadata: dict[str, Any] | None = None


def apply_channel_map(recording: Recording, rules: list[ChannelRule], *, keep_unmapped: bool = False) -> Recording:
    out = Recording(metadata=dict(recording.metadata), events=list(recording.events), history=list(recording.history))
    mapped_sources = set()
    for rule in rules:
        if rule.source not in recording.signals:
            raise KeyError(f"Configured source channel not found: {rule.source}")
        src = recording.signals[rule.source]
        data = np.asarray(src.data, dtype=float) * rule.scale + rule.offset
        if rule.invert:
            data = -data
        meta = dict(src.metadata)
        if rule.metadata:
            meta.update(rule.metadata)
        meta.update({"mapped_from": rule.source, "scale": rule.scale, "offset": rule.offset, "invert": rule.invert})
        out.add_signal(Signal(rule.name, data, src.fs, rule.unit, src.start_time_s, rule.signal_type, meta))
        mapped_sources.add(rule.source)

    if keep_unmapped:
        for name, sig in recording.signals.items():
            if name not in mapped_sources and name not in out.signals:
                out.add_signal(sig)

    out.record_step("apply_channel_map", rules=[r.__dict__ for r in rules], keep_unmapped=keep_unmapped)
    return out

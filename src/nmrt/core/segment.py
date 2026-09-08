from __future__ import annotations

from dataclasses import replace

from .model import Recording, Signal


def segment_signal(signal: Signal, start_s: float, end_s: float, *, name: str | None = None) -> Signal:
    if end_s <= start_s:
        raise ValueError("end_s must exceed start_s")
    i0 = max(0, round((start_s - signal.start_time_s) * signal.fs))
    i1 = min(signal.n_samples, round((end_s - signal.start_time_s) * signal.fs))
    if i1 <= i0:
        raise ValueError("Requested segment does not overlap signal")
    return replace(signal, name=name or signal.name, data=signal.data[i0:i1], start_time_s=start_s)


def segment_recording(recording: Recording, start_s: float, end_s: float) -> Recording:
    out = Recording(metadata=dict(recording.metadata), history=list(recording.history))
    for sig in recording.signals.values():
        try:
            out.add_signal(segment_signal(sig, start_s, end_s))
        except ValueError:
            pass
    out.events = [e for e in recording.events if start_s <= e.time_s < end_s]
    out.record_step("segment", start_s=start_s, end_s=end_s)
    return out

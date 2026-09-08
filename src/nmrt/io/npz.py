from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from nmrt.core.model import Event, Recording, Signal


def save_npz(recording: Recording, path: str | Path) -> None:
    payload = {f"signal__{k}": v.data for k, v in recording.signals.items()}
    meta = {
        "signals": {k: {"fs": v.fs, "unit": v.unit, "start_time_s": v.start_time_s,
                         "signal_type": v.signal_type, "metadata": v.metadata}
                    for k, v in recording.signals.items()},
        "events": [e.__dict__ for e in recording.events],
        "metadata": recording.metadata,
        "history": recording.history,
    }
    payload["__nmrt_metadata_json"] = np.array(json.dumps(meta))
    np.savez_compressed(path, **payload)


def load_npz(path: str | Path) -> Recording:
    z = np.load(path, allow_pickle=False)
    meta = json.loads(str(z["__nmrt_metadata_json"]))
    rec = Recording(metadata=meta.get("metadata", {}), history=meta.get("history", []))
    for name, sm in meta["signals"].items():
        rec.add_signal(Signal(name, z[f"signal__{name}"], sm["fs"], sm["unit"], sm["start_time_s"],
                              sm["signal_type"], sm.get("metadata", {})))
    rec.events = [Event(**e) for e in meta.get("events", [])]
    return rec

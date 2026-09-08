from __future__ import annotations

from pathlib import Path

import pandas as pd

from nmrt.core.model import Recording, Signal


def read_table(path: str | Path, *, fs: float, time_column: str | None = None,
               signal_types: dict[str, str] | None = None, units: dict[str, str] | None = None) -> Recording:
    path = Path(path)
    sep = "\t" if path.suffix.lower() in {".tsv", ".txt"} else ","
    df = pd.read_csv(path, sep=sep)
    rec = Recording(metadata={"source_path": str(path)})
    signal_types = signal_types or {}
    units = units or {}
    for col in df.columns:
        if col == time_column:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            rec.add_signal(Signal(col, df[col].to_numpy(float), fs, unit=units.get(col, "a.u."),
                                  signal_type=signal_types.get(col, "generic")))
    rec.record_step("read_table", path=str(path), fs=fs, time_column=time_column)
    return rec


def write_long_csv(recording: Recording, path: str | Path) -> None:
    rows = []
    for name, sig in recording.signals.items():
        for t, value in zip(sig.time_s, sig.data):
            rows.append({"signal": name, "time_s": t, "value": value, "unit": sig.unit,
                         "signal_type": sig.signal_type})
    pd.DataFrame(rows).to_csv(path, index=False)

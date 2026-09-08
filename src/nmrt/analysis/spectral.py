from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from scipy import signal


def welch_psd(x: np.ndarray, fs: float, nperseg: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    if nperseg is None:
        nperseg = min(len(x), max(256, round(fs * 4)))
    return signal.welch(x, fs=fs, nperseg=nperseg, detrend="constant")


def band_powers(x: np.ndarray, fs: float, bands: Iterable[tuple[float, float]]) -> dict[str, float]:
    f, pxx = welch_psd(x, fs)
    out: dict[str, float] = {}
    for low, high in bands:
        if high <= low:
            raise ValueError("Band upper bound must exceed lower bound")
        mask = (f >= low) & (f < high)
        key = f"{low:g}-{high:g}Hz"
        n_bins = np.count_nonzero(mask)
        if n_bins >= 2:
            out[key] = float(np.trapezoid(pxx[mask], f[mask]))
        elif n_bins == 1 and len(f) > 1:
            out[key] = float(pxx[mask][0] * np.median(np.diff(f)))
        else:
            out[key] = float("nan")
    return out


def coherence(x: np.ndarray, y: np.ndarray, fs: float, nperseg: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = min(len(x), len(y))
    if nperseg is None:
        nperseg = min(n, max(256, round(fs * 4)))
    return signal.coherence(x[:n], y[:n], fs=fs, nperseg=nperseg)

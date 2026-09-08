from __future__ import annotations

import numpy as np


def rms_db(x: np.ndarray, reference: float = 1.0) -> float:
    x = np.asarray(x, dtype=float)
    rms = np.sqrt(np.mean(x**2))
    if rms <= 0 or reference <= 0:
        return float("-inf")
    return float(20 * np.log10(rms / reference))


def estimate_f0_autocorr(x: np.ndarray, fs: float, fmin: float = 70.0, fmax: float = 500.0) -> float:
    x = np.asarray(x, dtype=float)
    x = x - np.mean(x)
    if np.allclose(x, 0):
        return float("nan")
    ac = np.correlate(x, x, mode="full")[len(x)-1:]
    min_lag = max(1, int(fs / fmax))
    max_lag = min(len(ac)-1, int(fs / fmin))
    if max_lag <= min_lag:
        return float("nan")
    lag = min_lag + int(np.argmax(ac[min_lag:max_lag + 1]))
    return float(fs / lag)

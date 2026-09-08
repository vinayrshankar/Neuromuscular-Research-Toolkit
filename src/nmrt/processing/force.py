from __future__ import annotations

import numpy as np

from nmrt.analysis.variability import approximate_entropy, coefficient_of_variation

from .common import butter_lowpass


def clean_force(x: np.ndarray, fs: float, lowpass_hz: float = 20.0) -> np.ndarray:
    return butter_lowpass(np.asarray(x, dtype=float), fs, lowpass_hz)


def yank(x: np.ndarray, fs: float) -> np.ndarray:
    return np.gradient(np.asarray(x, dtype=float), 1 / fs)


def force_features(x: np.ndarray, fs: float, mean_target: float | None = None,
                   lowpass_hz: float = 20.0) -> dict[str, float]:
    y = clean_force(x, fs, lowpass_hz)
    mean = float(np.mean(y))
    sd = float(np.std(y, ddof=1))
    rms = float(np.sqrt(np.mean(y**2)))
    dy = yank(y, fs)
    yank_rms = float(np.sqrt(np.mean(dy**2)))
    denom = abs(mean_target) if mean_target not in (None, 0) else abs(mean)
    normalized_yank = float(yank_rms / denom) if denom else float("nan")
    return {
        "mean": mean,
        "sd": sd,
        "cv_percent": coefficient_of_variation(y),
        "rms": rms,
        "yank_rms": yank_rms,
        "normalized_yank_rms": normalized_yank,
        "approximate_entropy": approximate_entropy(y),
    }

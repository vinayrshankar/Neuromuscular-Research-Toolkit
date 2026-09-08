from __future__ import annotations

import numpy as np

from .common import butter_bandpass, butter_lowpass, moving_rms, notch


def clean_emg(x: np.ndarray, fs: float, bandpass_hz: tuple[float, float] = (20, 450),
              notch_hz: float | None = None) -> np.ndarray:
    y = butter_bandpass(x, fs, bandpass_hz[0], bandpass_hz[1])
    if notch_hz is not None:
        y = notch(y, fs, notch_hz)
    return y


def emg_envelope(x: np.ndarray, fs: float, bandpass_hz: tuple[float, float] = (20, 450),
                 envelope_hz: float = 6.0, notch_hz: float | None = None) -> np.ndarray:
    cleaned = clean_emg(x, fs, bandpass_hz, notch_hz)
    return butter_lowpass(np.abs(cleaned), fs, envelope_hz)


def emg_features(x: np.ndarray, fs: float, rms_window_ms: float = 100.0) -> dict[str, float]:
    x = np.asarray(x, dtype=float)
    finite = x[np.isfinite(x)]
    if finite.size == 0:
        return {k: float("nan") for k in ("rms", "mav", "iemg")}
    rms = float(np.sqrt(np.mean(finite**2)))
    mav = float(np.mean(np.abs(finite)))
    iemg = float(np.trapezoid(np.abs(finite), dx=1 / fs))
    moving = moving_rms(finite, fs, rms_window_ms)
    return {
        "rms": rms,
        "mav": mav,
        "iemg": iemg,
        "moving_rms_mean": float(np.mean(moving)),
    }

from __future__ import annotations

import numpy as np
from scipy import signal


def _normalized(freq: float, fs: float) -> float:
    if not 0 < freq < fs / 2:
        raise ValueError(f"Cutoff {freq} Hz must be between 0 and Nyquist ({fs/2:g} Hz)")
    return freq / (fs / 2)


def butter_lowpass(x: np.ndarray, fs: float, cutoff_hz: float, order: int = 4) -> np.ndarray:
    sos = signal.butter(order, _normalized(cutoff_hz, fs), btype="low", output="sos")
    return signal.sosfiltfilt(sos, np.asarray(x, dtype=float))


def butter_highpass(x: np.ndarray, fs: float, cutoff_hz: float, order: int = 4) -> np.ndarray:
    sos = signal.butter(order, _normalized(cutoff_hz, fs), btype="high", output="sos")
    return signal.sosfiltfilt(sos, np.asarray(x, dtype=float))


def butter_bandpass(x: np.ndarray, fs: float, low_hz: float, high_hz: float, order: int = 4) -> np.ndarray:
    if high_hz <= low_hz:
        raise ValueError("high_hz must exceed low_hz")
    sos = signal.butter(order, [_normalized(low_hz, fs), _normalized(high_hz, fs)], btype="band", output="sos")
    return signal.sosfiltfilt(sos, np.asarray(x, dtype=float))


def notch(x: np.ndarray, fs: float, freq_hz: float = 60.0, q: float = 30.0) -> np.ndarray:
    b, a = signal.iirnotch(freq_hz, q, fs=fs)
    return signal.filtfilt(b, a, np.asarray(x, dtype=float))


def moving_rms(x: np.ndarray, fs: float, window_ms: float = 100.0) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    n = max(1, round(window_ms / 1000 * fs))
    kernel = np.ones(n) / n
    return np.sqrt(np.convolve(x * x, kernel, mode="same"))

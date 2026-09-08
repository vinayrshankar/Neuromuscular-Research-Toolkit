from __future__ import annotations

import numpy as np

from .common import butter_lowpass


def breathing_phases(flow: np.ndarray, fs: float, lowpass_hz: float = 5.0,
                     deadband_fraction: float = 0.02) -> dict[str, np.ndarray]:
    """Classify filtered flow into inspiration (+1), expiration (-1), and pause (0).

    Sign convention is user-configurable by multiplying the input by -1 before calling when needed.
    """
    y = butter_lowpass(np.asarray(flow, dtype=float), fs, lowpass_hz)
    scale = np.nanpercentile(np.abs(y), 95)
    threshold = deadband_fraction * scale
    phase = np.zeros(len(y), dtype=int)
    phase[y > threshold] = 1
    phase[y < -threshold] = -1
    return {"filtered_flow": y, "phase": phase}

from __future__ import annotations

import numpy as np


def vector_magnitude(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    return np.sqrt(np.asarray(x, dtype=float)**2 + np.asarray(y, dtype=float)**2 + np.asarray(z, dtype=float)**2)

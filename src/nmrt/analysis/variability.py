from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree


def coefficient_of_variation(x: np.ndarray, ddof: int = 1) -> float:
    x = np.asarray(x, dtype=float)
    mean = float(np.nanmean(x))
    if np.isclose(mean, 0.0):
        return float("nan")
    return float(np.nanstd(x, ddof=ddof) / abs(mean) * 100.0)


def approximate_entropy(x: np.ndarray, m: int = 2, r: float | None = None) -> float:
    """Approximate entropy (ApEn) using Chebyshev-distance template matching.

    Uses a cKDTree neighbor search rather than materializing an O(N^2) distance
    matrix, which makes typical neuromuscular trial lengths practical.
    Self-matches are retained, consistent with the standard ApEn definition.
    """
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n <= m + 1:
        return float("nan")
    sd = float(np.std(x))
    if sd == 0:
        return 0.0
    if r is None:
        r = 0.2 * sd
    if r <= 0:
        raise ValueError("r must be > 0")

    def phi(mm: int) -> float:
        windows = np.lib.stride_tricks.sliding_window_view(x, mm)
        tree = cKDTree(windows)
        counts = tree.query_ball_point(windows, r=r, p=np.inf, return_length=True)
        proportions = counts / len(windows)
        return float(np.mean(np.log(np.maximum(proportions, np.finfo(float).tiny))))

    return phi(m) - phi(m + 1)

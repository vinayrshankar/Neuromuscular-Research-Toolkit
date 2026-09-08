from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .model import Recording, Signal


@dataclass(frozen=True)
class QCResult:
    signal: str
    passed: bool
    nan_fraction: float
    std: float
    robust_outlier_fraction: float
    clipping_proxy_fraction: float
    messages: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def signal_qc(
    signal: Signal,
    *,
    max_nan_fraction: float = 0.001,
    flat_std_threshold: float = 1e-10,
    max_robust_outlier_fraction: float = 0.02,
    max_clipping_proxy_fraction: float = 0.02,
) -> QCResult:
    x = np.asarray(signal.data, dtype=float)
    finite = np.isfinite(x)
    nan_fraction = float(1 - finite.mean()) if x.size else 1.0
    xf = x[finite]
    messages: list[str] = []

    if xf.size == 0:
        return QCResult(signal.name, False, nan_fraction, float("nan"), 1.0, 1.0,
                        ("No finite samples",))

    std = float(np.std(xf))
    median = float(np.median(xf))
    mad = float(np.median(np.abs(xf - median)))
    if mad > 0:
        robust_z = 0.6744897501960817 * (xf - median) / mad
        outlier_fraction = float(np.mean(np.abs(robust_z) > 8.0))
    else:
        outlier_fraction = 0.0

    xmin, xmax = float(np.min(xf)), float(np.max(xf))
    clipping_fraction = float(max(np.mean(xf == xmin), np.mean(xf == xmax))) if xmax > xmin else 1.0

    passed = True
    if nan_fraction > max_nan_fraction:
        passed = False
        messages.append(f"NaN fraction {nan_fraction:.4g} exceeds {max_nan_fraction:.4g}")
    if std <= flat_std_threshold:
        passed = False
        messages.append("Signal is flat or nearly flat")
    if outlier_fraction > max_robust_outlier_fraction:
        passed = False
        messages.append("Robust outlier fraction exceeds threshold")
    if clipping_fraction > max_clipping_proxy_fraction:
        passed = False
        messages.append("Repeated-extreme clipping proxy exceeds threshold")
    if not messages:
        messages.append("QC checks passed")

    return QCResult(
        signal.name,
        passed,
        nan_fraction,
        std,
        outlier_fraction,
        clipping_fraction,
        tuple(messages),
    )


def recording_qc(recording: Recording, **kwargs) -> list[QCResult]:
    return [signal_qc(sig, **kwargs) for sig in recording.signals.values()]

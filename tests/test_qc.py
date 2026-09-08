import numpy as np

from nmrt.core.model import Signal
from nmrt.core.qc import signal_qc


def test_qc_passes_noise():
    rng = np.random.default_rng(1)
    q = signal_qc(Signal("x", rng.normal(size=10000), 1000))
    assert q.passed


def test_qc_flags_flat_signal():
    q = signal_qc(Signal("flat", np.ones(1000), 1000))
    assert not q.passed

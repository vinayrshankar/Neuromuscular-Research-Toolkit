import numpy as np

from nmrt.core.model import Event, Recording, Signal
from nmrt.core.segment import segment_signal


def test_signal_time_and_duration():
    s = Signal("x", np.arange(1000), fs=1000, unit="V")
    assert s.n_samples == 1000
    assert s.duration_s == 1.0
    assert np.isclose(s.time_s[-1], 0.999)


def test_recording_require_and_event_sort():
    r = Recording()
    r.add_signal(Signal("x", np.arange(10), fs=10))
    r.add_event(Event("b", 2.0))
    r.add_event(Event("a", 1.0))
    assert r.require("x")[0].name == "x"
    assert [e.name for e in r.events] == ["a", "b"]


def test_segment_signal():
    s = Signal("x", np.arange(1000), fs=1000)
    seg = segment_signal(s, 0.2, 0.7)
    assert len(seg.data) == 500
    assert np.isclose(seg.start_time_s, 0.2)

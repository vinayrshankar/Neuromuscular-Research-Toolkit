from __future__ import annotations

import numpy as np

from nmrt.core.model import Event, Recording, Signal


def make_force_emg_demo(duration_s: float = 30.0, fs: float = 1000.0, seed: int = 7) -> Recording:
    rng = np.random.default_rng(seed)
    t = np.arange(int(duration_s * fs)) / fs
    force = 10 + 0.25*np.sin(2*np.pi*0.25*t) + 0.08*np.sin(2*np.pi*1.2*t) + 0.05*rng.standard_normal(len(t))
    carrier = rng.standard_normal(len(t))
    modulation = 0.4 + 0.12*np.sin(2*np.pi*0.25*t)
    emg = modulation * carrier + 0.05*np.sin(2*np.pi*60*t)
    accx = 0.02*rng.standard_normal(len(t))
    accy = 0.02*rng.standard_normal(len(t))
    accz = 1 + 0.02*rng.standard_normal(len(t))

    rec = Recording(metadata={"synthetic": True, "task": "sustained_force"})
    rec.add_signal(Signal("Force", force, fs, unit="%MVC", signal_type="force"))
    rec.add_signal(Signal("TA_EMG", emg, fs, unit="mV", signal_type="emg"))
    rec.add_signal(Signal("ACC_X", accx, fs, unit="g", signal_type="acc"))
    rec.add_signal(Signal("ACC_Y", accy, fs, unit="g", signal_type="acc"))
    rec.add_signal(Signal("ACC_Z", accz, fs, unit="g", signal_type="acc"))
    rec.add_event(Event("steady_state_start", 5.0))
    rec.add_event(Event("steady_state_end", duration_s - 5.0))
    rec.record_step("synthetic_generation", duration_s=duration_s, fs=fs, seed=seed)
    return rec

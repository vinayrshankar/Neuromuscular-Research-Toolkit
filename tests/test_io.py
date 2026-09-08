from pathlib import Path

import numpy as np

from nmrt.io.npz import load_npz, save_npz
from nmrt.synthetic import make_force_emg_demo


def test_npz_roundtrip(tmp_path: Path):
    rec = make_force_emg_demo(duration_s=2, fs=100)
    p = tmp_path / "demo.npz"
    save_npz(rec, p)
    loaded = load_npz(p)
    assert set(loaded.signals) == set(rec.signals)
    assert np.allclose(loaded.signals["Force"].data, rec.signals["Force"].data)
    assert loaded.signals["Force"].unit == "%MVC"

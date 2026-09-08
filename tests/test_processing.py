import numpy as np

from nmrt.analysis.spectral import band_powers, coherence
from nmrt.analysis.variability import approximate_entropy, coefficient_of_variation
from nmrt.processing.audio import estimate_f0_autocorr
from nmrt.processing.emg import emg_features
from nmrt.processing.force import force_features, yank
from nmrt.processing.imu import vector_magnitude


def test_cv_known_signal():
    x = np.array([9.0, 10.0, 11.0])
    assert np.isclose(coefficient_of_variation(x), 10.0)


def test_apen_constant_zero():
    assert approximate_entropy(np.ones(100)) == 0.0


def test_yank_linear_signal():
    fs = 1000
    t = np.arange(1000)/fs
    y = yank(3*t, fs)
    assert np.allclose(y[10:-10], 3, atol=1e-10)


def test_force_features_constant_like():
    fs = 1000
    t = np.arange(5000)/fs
    x = 10 + 0.1*np.sin(2*np.pi*1*t)
    f = force_features(x, fs, mean_target=10)
    assert abs(f["mean"] - 10) < 1e-3
    assert f["sd"] > 0
    assert f["yank_rms"] > 0


def test_emg_features_known_rms():
    fs = 1000
    t = np.arange(1000)/fs
    x = np.sin(2*np.pi*100*t)
    f = emg_features(x, fs)
    assert np.isclose(f["rms"], 1/np.sqrt(2), atol=1e-3)


def test_band_power_finds_one_hz_component():
    fs = 100
    t = np.arange(2000)/fs
    x = np.sin(2*np.pi*1*t)
    b = band_powers(x, fs, [(0.5, 1.5), (2, 5)])
    assert b["0.5-1.5Hz"] > b["2-5Hz"]


def test_coherence_same_signal_high_at_frequency():
    fs = 200
    t = np.arange(4000)/fs
    x = np.sin(2*np.pi*10*t)
    f, c = coherence(x, x, fs)
    idx = np.argmin(np.abs(f-10))
    assert c[idx] > 0.99


def test_imu_vector_magnitude():
    mag = vector_magnitude(np.array([3]), np.array([4]), np.array([0]))
    assert np.isclose(mag[0], 5)


def test_f0_estimate():
    fs = 5000
    t = np.arange(fs)/fs
    x = np.sin(2*np.pi*200*t)
    f0 = estimate_f0_autocorr(x, fs)
    assert abs(f0-200) < 5

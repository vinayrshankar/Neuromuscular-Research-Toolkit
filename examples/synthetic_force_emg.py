from pprint import pprint

from nmrt.analysis.spectral import band_powers
from nmrt.processing.emg import emg_envelope, emg_features
from nmrt.processing.force import force_features
from nmrt.synthetic import make_force_emg_demo

rec = make_force_emg_demo()
force, emg = rec.require("Force", "TA_EMG")

envelope = emg_envelope(emg.data, emg.fs)
print(f"Generated {force.duration_s:.1f} s synthetic recording with {len(rec.signals)} channels")
print(f"EMG envelope samples: {len(envelope)}")
print("\nForce features")
pprint(force_features(force.data, force.fs, mean_target=10.0))
print("\nEMG features")
pprint(emg_features(emg.data, emg.fs))
print("\nForce PSD bands")
pprint(band_powers(force.data, force.fs, [(0, 0.5), (0.5, 1), (1, 1.5), (1.5, 2), (2, 10)]))

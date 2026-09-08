from __future__ import annotations

from pathlib import Path

import yaml

from nmrt.analysis.spectral import band_powers, coherence
from nmrt.core.qc import recording_qc
from nmrt.processing.emg import emg_features
from nmrt.processing.force import force_features
from nmrt.reporting.export import export_results
from nmrt.synthetic import make_force_emg_demo


def run_recipe(path: str | Path) -> dict:
    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    inp = cfg["input"]
    if inp["type"] != "synthetic_force_emg":
        raise NotImplementedError("v0.1 recipe runner currently ships with the synthetic demo input")
    rec = make_force_emg_demo(inp.get("duration_s", 30), inp.get("fs", 1000))

    qc_cfg = cfg.get("qc", {})
    qcs = recording_qc(rec, **qc_cfg)
    analysis = cfg["analysis"]
    force, emg = rec.require(analysis["force_channel"], analysis["emg_channel"])

    results = {
        "metadata": rec.metadata,
        "qc": {q.signal: q.to_dict() for q in qcs},
        "force": force_features(force.data, force.fs, mean_target=analysis.get("force_target"),
                                lowpass_hz=analysis.get("force_lowpass_hz", 20)),
        "emg": emg_features(emg.data, emg.fs),
        "force_psd_bands": band_powers(force.data, force.fs, [tuple(b) for b in analysis.get("psd_bands", [])]),
    }
    if force.fs == emg.fs:
        f, cxy = coherence(force.data, emg.data, force.fs)
        results["force_emg_coherence"] = {
            "peak_coherence": float(cxy.max()),
            "peak_frequency_hz": float(f[cxy.argmax()]),
        }

    export_results(results, cfg.get("output", {}).get("directory", "nmrt_output"))
    return results

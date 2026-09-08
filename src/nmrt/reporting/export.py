from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def export_results(results: dict[str, Any], output_dir: str | Path, stem: str = "nmrt_results") -> tuple[Path, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / f"{stem}.json"
    csv_path = out / f"{stem}.csv"
    json_path.write_text(json.dumps(results, indent=2, default=_json_default), encoding="utf-8")

    flat_rows = []
    for section, values in results.items():
        if isinstance(values, dict):
            for metric, value in values.items():
                if not isinstance(value, (dict, list, tuple)):
                    flat_rows.append({"section": section, "metric": metric, "value": value})
    pd.DataFrame(flat_rows).to_csv(csv_path, index=False)
    return json_path, csv_path


def _json_default(value):
    try:
        return value.item()
    except AttributeError:
        return str(value)

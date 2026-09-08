# Architecture

NMRT uses a layered architecture so acquisition, analysis and user interface code do not become tightly coupled.

## Layers

1. **Core** — canonical data model, metadata, provenance, QC contracts.
2. **I/O** — file/device adapters that convert vendor formats into the canonical model.
3. **Processing** — deterministic signal transforms.
4. **Analysis** — feature extraction and cross-signal metrics.
5. **Pipeline** — YAML-driven batch execution.
6. **Reporting** — tables, JSON provenance, figures and future HTML/PDF reports.
7. **GUI** — a future desktop workbench that calls the same APIs.

## Canonical object hierarchy

`Recording` contains `Signal` objects plus `Event` markers and a processing history. A `Signal` owns a NumPy array and explicit sampling frequency, units, start time and metadata.

Future project-level hierarchy:

`Project → Participant → Session → Task → Trial → Recording/Signal`

Participant identifiers should be pseudonymous/deidentified when exported.

## Raw vs processed data

Raw imported/acquired data should never be mutated in place. Processing functions return arrays or derived `Signal` instances. Exported provenance should record source hashes, software version, recipe hash, preprocessing parameters and exclusions.

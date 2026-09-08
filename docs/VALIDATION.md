# Validation Framework

Scientific software should distinguish between a function existing and a function being validated.

## Validation tiers

### Tier 0 — Experimental
Algorithm is implemented but has not yet completed a reference comparison.

### Tier 1 — Analytical
Validated using synthetic signals with known mathematical properties.

### Tier 2 — Cross-implementation
Compared against a trusted independent implementation using fixed input data and tolerances.

### Tier 3 — Workflow regression
Validated using frozen synthetic or permission-cleared example datasets across an entire pipeline.

### Tier 4 — Hardware/system validation
Timing, scaling or acquisition behavior validated against physical test equipment or a documented laboratory procedure.

Each public metric should eventually expose its validation tier in the documentation.

## Initial v0.1 checks

Current automated tests cover:
- sampling/duration behavior
- segmentation
- CV on a known signal
- approximate entropy on a constant signal
- derivative/yank on a linear ramp
- force statistics on a known oscillation
- EMG RMS on a sinusoid
- PSD band localization
- coherence of identical signals
- vector magnitude
- F0 estimation for a synthetic tone
- QC pass/fail behavior
- NPZ round trip

These are foundation tests, not a complete scientific validation package.

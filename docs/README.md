# NMRT Documentation

This documentation is organized around the scientific and engineering decisions that make NMRT reproducible rather than around one laboratory's study names.

## Start here

- [Architecture](ARCHITECTURE.md) — layers, canonical data model, provenance, and raw/processed separation
- [Validation framework](VALIDATION.md) — validation tiers and current automated checks
- [Hardware and vendor adapters](HARDWARE_ADAPTERS.md) — Delsys, NI, CED/Spike2, LabChart, and synchronization strategy
- [Ultimate roadmap](ULTIMATE_ROADMAP.md) — planned path from scientific core to full research workbench

## Repository guides

- [README](../README.md) — installation, quick start, capabilities, and project overview
- [Contributing](../CONTRIBUTING.md) — contribution expectations for scientific software
- [Support](../SUPPORT.md) — how to ask for help without exposing research data
- [Security](../SECURITY.md) — vulnerability and sensitive-data reporting
- [Release checklist](../RELEASE_CHECKLIST.md) — scientific and software checks before a release

## Documentation principles

NMRT documentation should always state:

- the expected signal type and units;
- sampling-frequency assumptions;
- preprocessing parameters;
- what an algorithm can and cannot infer;
- validation status;
- whether a feature requires optional vendor software or hardware;
- whether timing is software-estimated or hardware-validated.

Study-specific examples must use synthetic or permission-cleared data.

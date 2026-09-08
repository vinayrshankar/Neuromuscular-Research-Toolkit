# Contributing

Contributions are welcome. NMRT is scientific software, so changes that affect numerical results need more than code style.

## Expectations

- Add or update tests for numerical behavior.
- Document units, sampling assumptions and edge cases.
- Avoid hard-coded study names, muscles, participants or folder structures.
- Do not add participant data to tests or examples.
- Record references for scientific formulas or algorithm choices.
- Keep vendor-specific logic inside adapters.
- Mark algorithms experimental if validation is incomplete.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src tests
```

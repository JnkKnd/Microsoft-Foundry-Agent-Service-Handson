---
description: Placement of unit, contract, and runtime checks; external I/O isolation and result reporting.
applyTo: "tests/**"
---

# Test changes

- Use `tests/unit/` for functions, domain logic, and failure handling;
  `tests/contract/` checks API, materials, Notebook, and template consistency.
  Reuse existing `conftest.py` files and fixtures.
- Use pytest with `test_*.py` / `test_*` naming. State expected contract values
  explicitly rather than merely copying implementation calculations.
- Use `tmp_path`, `monkeypatch`, and existing FakeRunner / SDK fakes to isolate
  Azure, authentication, network, and subprocess I/O at appropriate boundaries.
  Unit and contract tests must not connect to live environments.
- In addition to normal cases, cover relevant invalid input, external failures,
  and retry limits. Validation logic needs tests that reject deliberately broken input.
- Run Hosted tests in the dedicated Python 3.13 environment as well. Management
  environment skips for missing SDKs and successful fakes do not replace this check.
- Distinguish `tests/runtime/` container checks and live end-to-end verification
  from unit and contract tests. An `integration` marker is not approval to create
  environments or incur charges.
- Check executed counts, skips, and failures. Zero tests or unconditional success
  are not validation. See the [developer guide](../../docs/development/README.md)
  for environments and entry points.

Reference: [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html).

---
description: Python conventions for management scripts, Travel Ops API, and Hosted Agents.
applyTo: "**/*.py,**/pyproject.toml,**/requirements*.txt"
---

# Python changes

- The [root pyproject.toml](../../pyproject.toml) defines formatting, imports, and lint.
  Follow existing `snake_case` / `PascalCase` naming; do not add rules that conflict with Ruff.
- Follow each manifest's Python support range. Standard management and Travel Ops API
  run on 3.12; Hosted Agents run on 3.13. Root Ruff targets `py310`, so do not adopt
  Hosted-only syntax or SDKs across all management scripts.
- Annotate changed function parameters and returns consistently with existing types.
  Validate external JSON before use; do not hide mismatches with unnecessary `Any`
  or type-check suppression.
- Travel Ops API dependencies flow HTTP adapter → application → domain. Keep HTTP
  and framework types out of the domain; translate domain exceptions into HTTP
  responses in adapters. See the [API README](../../src/travel-api/README.md).
- Keep Hosted startup thin and place Agent definitions and workflows in existing
  modules. Check SDK and environment contracts in the
  [Hosted README](../../src/hosted-agent/README.md) and
  [requirements.txt](../../src/hosted-agent/requirements.txt).
- Reuse `scripts/lib/` connection and runtime helpers. Place I/O at replaceable
  test boundaries, catch only expected exceptions, bound retries, and never
  turn failures into empty values or successful-looking results.
- Use the existing [shared development environment](../../.devcontainer/README.md)
  for dependencies and kernels. Keep management and Hosted environments separate.
  Do not auto-install dependencies from scripts other than environment setup.

Reference: [Python type annotations](https://docs.python.org/3.12/library/typing.html).
Annotations and Ruff success do not prove that a dedicated static type check passed.

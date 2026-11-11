---
description: Maintain GitHub Actions and Makefile validation entry points, environments, and permissions.
applyTo: ".github/workflows/*.yml,.github/workflows/*.yaml,Makefile"
---

# CI and validation entry point changes

- Reuse [validate.yml](../workflows/validate.yml) and [Makefile](../../Makefile).
  Do not add pipelines with duplicate responsibilities. Keep validation commands
  consistent with the [developer guide](../../docs/development/README.md).
- Distinguish Python 3.12 management, Python 3.13 Hosted, Bicep, bootstrap image,
  Dev Container, and API container checks. Preserve runtime, dependency, and working
  directory mappings, and align local validation with CI.
- Check the impact of Bicep compiler updates on generated ARM and artifact equality.
  Cache keys and paths must match dependency files actually used by the job.
- Default ordinary validation to `contents: read`. Do not add unnecessary permissions,
  secrets, or persisted checkout credentials. Never give external PR code write
  permissions through `pull_request_target`.
- The [API publishing workflow](../workflows/publish-travel-api.yml) is separate
  from validation CI. Do not move publish permissions or push steps into validation
  or publish merely to check a configuration change.
- Verify official releases/tags and required runners when adding or updating Actions.
  Do not invent SHAs, hide failures with `continue-on-error`, or allow zero tests.
- Report static workflow checks, local equivalent checks, and remote CI success separately.

Reference: [Secure use of GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).

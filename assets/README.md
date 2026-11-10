# Shared materials (Lab 4)

Open each file on GitHub and select **Download raw file**.
Use the Skill ZIP for Skill upload in Foundry Portal without extracting it.

| Material | Shared file |
| --- | --- |
| Travel cost estimation Skill | [travel-estimation.zip](skills/travel-estimation.zip) |
| Preapproval simulation Skill | [preapproval-simulation.zip](skills/preapproval-simulation.zip) |
| Travel Ops API OpenAPI 3.1 | [travel-ops.openapi.json](openapi/travel-ops.openapi.json) |

Paste the OpenAPI into the Portal schema editor. Replace only
`https://replace-with-your-travel-api.example.invalid` in `servers[0].url` with
**Outputs → travelApiBaseUrl** from your ARM deployment. Do not change the rest of the schema.
API authentication is **Anonymous**. Shared files contain no environment or account information.

## Regeneration and validation

The sources of truth are `data/skills/<name>/SKILL.md` for Skills and
`app.openapi()` in `src/travel-api` for OpenAPI. Do not edit ZIP or JSON files directly.
Install the repository dependencies and the pinned API dependencies from
`src/travel-api/requirements.txt` in the Python 3.12 management environment, then run
from the repository root:

```console
python -B -m scripts.build_common_assets
python -B -m scripts.build_common_assets --check
```

Generation uses local source only. `--check` writes nothing and exits nonzero for
missing files, differences, or invalid source. When changing the API contract, also
check compatibility with the pinned image distributed for the workshop.
No environment-specific ZIP, `portal-values.json`, connection settings, or credentials are generated.

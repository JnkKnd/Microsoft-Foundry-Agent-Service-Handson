# Contoso Travel Ops API

[Developer guide](../../docs/development/README.md) / [Workshop architecture](../../docs/development/architecture.md)

A stateless mock API for the "Contoso travel and expenses" scenario in the Microsoft
Foundry Agent Service workshop. It uses no database, external calls, or randomness.
Responses are determined from requests and fixed in-memory data, allowing identical
conditions to be reproduced for agent evaluation and optimization.

## Structure and constraints

- `travel_api/domain` contains policy rules without I/O;
  `travel_api/application` contains framework-independent use cases;
  `travel_api/adapters/api` is the FastAPI adapter converting requests / responses
  and mapping them to HTTP status codes.
- Uses OpenAPI 3.1, with an `operationId` and typed Pydantic request / response
  models for each operation.
- `POST /preapprovals` is always a simulation. Decision values begin with
  `simulated_` and responses include a warning. It does not grant actual travel approval.
- No personal information is handled. Identifiers are only aliases for synthetic
  data, such as `employee-001`.

## Endpoints

| Method | Path | operationId | Purpose |
|---|---|---|---|
| GET | `/health` | `getHealth` | Check health and readiness |
| GET | `/per-diem?city=&date=` | `getPerDiem` | Per diem and lodging limits for a city / date |
| POST | `/trip-estimates` | `createTripEstimate` | Estimate airfare, lodging, and meal costs |
| POST | `/preapprovals` | `createPreapproval` | Simulated preapproval decision |

Interactive OpenAPI documentation is available at `/docs` (Swagger UI) and `/redoc`;
the JSON specification is at `/openapi.json`.

## Running locally

Requires Python 3.12. Run from this directory (`src/travel-api`).

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

uvicorn travel_api.main:app --host 0.0.0.0 --port 8080
```

Check responses from another Terminal:

```bash
curl http://127.0.0.1:8080/health
curl "http://127.0.0.1:8080/per-diem?city=Osaka&date=2026-05-11"
```

## Running with Docker

```bash
docker build -t travel-ops-api:local .
docker run --rm -p 8080:8080 \
  -e WORKSHOP_SOURCE_BASE=https://github.com/example/workshop/blob/main \
  travel-ops-api:local
curl http://127.0.0.1:8080/health
```

The container runs as a non-root user and listens on port 8080.
`HEALTHCHECK` uses the Python standard library to check `/health` because the
`-slim` base image has no `curl` / `wget`.
It uses no persistent volumes and can scale to zero between requests in Azure Container Apps.

`WORKSHOP_SOURCE_BASE` replaces the placeholder URL for policy references in responses.
It may be omitted for local runs where unresolved placeholder URLs are acceptable.

## Tests

This component's dependencies are separate from the root `pyproject.toml`.
See this directory's `requirements.txt` / `pyproject.toml`.
Install the API dependencies before running `tests/unit/travel_api/` and
`tests/contract/travel_api/`. This example starts at the repository root:

```bash
cd src/travel-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"

cd ../..
python -m pytest tests/unit/travel_api tests/contract/travel_api
```

Domain unit tests require only the `travel_api` package on `sys.path`, not FastAPI.
Contract tests for the HTTP layer and `/openapi.json` also require `fastapi` / `httpx`.
When missing, `pytest.importorskip` skips these tests, so root `make test` can run
before this component's dependencies are installed. Do not count skipped contract
tests as verified.

## Numerical consistency with policy data

Per diem and lodging limits in `travel_api/domain/rates.py` match the tables in
`data/policies/03-hotels.md` and `data/policies/04-per-diem-meals.md`.
`tests/contract/data/test_per_diem_rates_match_policy.py` reads the Markdown tables
and checks numerical agreement with the implementation. Preserve this contract
when changing either policies or the API.

## Publishing the container

The [publication workflow](../../.github/workflows/publish-travel-api.yml) builds and
pushes a public GHCR image on `travel-api-v*` tags or manual dispatch.
Published tags do not use `latest`. Set the workshop Bicep `travelApiImageRef` to
the immutable digest reference printed in the job summary.
See the [infrastructure implementation guide](../../infra/README.md) for updates.

The English release source SHA and API image have not yet been published.
Publication requires a separately approved release operation; documentation
translation does not publish an image or establish release readiness. Use the
approved JnkKnd English release only after its public source SHA and image digest
have been verified; do not substitute a mutable branch for the bootstrap pin.

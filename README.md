# pysmartdok

A Python library for the [SmartDok API](https://api.smartdok.no/api-docs/).

## Installation
To use in a project, add this to dependencies in `pyproject.toml`:

```
"pysmartdok @ git+https://github.com/asterisk-digital/pysmartdok.git@main"
```

## Usage

Uses the SmartDok REST API. Requires an API token.

```python
import pysmartdok

client = pysmartdok.ApiClient(
    api_token="your_api_token",
    user_agent="myapp(you@example.com)",  # optional, defaults to "pysmartdok"
)

# Quality Deviations
qd_reports = client.qd.get_qd_reports(
    project_id=123,        # optional
    qd_status="Open",      # optional: Open, Close, Unprocessed, Discarded
)
qd_pdf = client.qd.get_qd_pdf(qd_id=789, include_details=True)

# Projects
projects = client.projects.get_projects(include_inactive=False, include_orders=False)
project = client.projects.get_project(project_id=123)
subprojects = client.projects.get_subprojects(project_id=123)
next_number = client.projects.get_next_project_number()

# RUE summaries (paginates internally, returns all matching reports)
summaries = client.rue.get_rue_summaries(
    project_id=123,                              # optional
    rue_status="Open",                           # optional: Open, Close, Unprocessed, Discarded
    last_updated_since="2024-01-01T00:00:00Z",   # optional
)

# Single RUE report (full detail)
report = client.rue.get_rue_report(rue_id=456)

# All full RUE reports — fetches summaries then fans out concurrently
reports = client.rue.get_rue_reports(threads=8)

# RUE event log (audit trail)
events = client.rue.get_rue_eventlog(rue_id=456)

# RUE messages/comments
messages = client.rue.get_rue_messages(rue_id=456)

# RUE PDF metadata
pdf_info = client.rue.get_rue_pdf(rue_id=456, include_details=True)

# Users
users = client.users.get_users(include_inactive=False)
me = client.users.get_current_user()
user = client.users.get_user(user_id="...")
license_info = client.users.get_license_info()
```

## Development

Set up the environment with [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv sync
```

Before pushing, run lint, format, and tests — CI runs the same on Python 3.13 and 3.14:

```bash
uv run ruff check .
uv run ruff format .
uv run tox
```

Tests use `responses` to mock the SmartDok API; no token is needed. To smoke-test against the real API, drop a `.env` at the repo root with `SMARTDOK_API_KEY=...` and run one of the scripts in `scripts/`:

```bash
uv run python scripts/get_rue_summaries.py
```

### Change conventions

- All changes must conform to the SmartDok OpenAPI spec, which is vendored at `docs/swagger.json`. Refresh it from upstream when SmartDok updates the API; commit the diff so spec changes are visible in git history:
  ```bash
  curl https://api.smartdok.no/docs/v1 -o docs/swagger.json
  ```
- New endpoints: add a Pydantic model in `rue_models.py` (or a new module) with Norwegian field descriptions matching the SmartDok web UI; add the method to the relevant subclient (`Rue`, `Users`, or `ApiClient`); add a mocked test in `tests/test_basic.py`.
- Public methods get short docstrings; field descriptions live on the Pydantic model.
- Runtime deps go in `[project.dependencies]` with `>=` bounds; dev deps go in `[dependency-groups.dev]` with exact pins.
- Update `README.md` and `CHANGELOG.md` for any user-visible change.

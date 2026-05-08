# pysmartdok

A Python library for SmartDok' API. Under active development.

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
qd_items = client.get_qd()

# Projects
projects = client.get_projects()

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

### Setup

To set up the python environment you need [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:
```(bash)
uv sync
```

### Run linter

```(bash)
uv run ruff check .
```

### Run tests

```(bash)
uv run tox
```

### Run formatter

```(bash)
uv run ruff format .
```

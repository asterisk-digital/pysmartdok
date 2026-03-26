# pysmartdok

A Python library for SmartDok' API. Under active development.

## Installation
To use in a project, add this in dependencies in pyproject.toml:

```
"pysmartdok @ git+ssh://git@github.com/asterisk-digital/pysmartdok.git@main"
```

## Usage

### ApiClient

Uses the SmartDok REST API. Requires an API token.

```python
import pysmartdok

client = pysmartdok.ApiClient(api_token="your_api_token")

# Quality Deviations
qd_items = client.get_qd()

# Projects
projects = client.get_projects()

# RUE summaries (paginated, replaces deprecated GET /rue)
summaries = client.get_rue_summaries(
    project_id=123,           # optional
    rue_status="Open",        # optional: Open, Close, Unprocessed, Discarded
    last_updated_since="2024-01-01T00:00:00Z",  # optional
    offset=0,                 # optional, default 0
    count=100,                # optional, default 100 (max 100)
)

# Single RUE report (full detail)
report = client.get_rue_report(rue_id=456)

# RUE event log (audit trail)
events = client.get_rue_eventlog(rue_id=456)

# RUE messages/comments
messages = client.get_rue_messages(rue_id=456)

# RUE PDF
pdf_info = client.get_rue_pdf(rue_id=456, include_details=True)
# Returns: {"Filename": "...", "DownloadUrl": "...", "FileSize": ..., "FileDate": "..."}
```

> **Note:** `get_rue()` still works but is deprecated — it will emit a `DeprecationWarning` and log a warning. Use `get_rue_summaries()` instead.

### WebClient

Uses web scraping via the SmartDok web interface. Requires username and password.

```python
import pysmartdok

client = pysmartdok.WebClient(username="your_username", password="your_password")

# Get all records of a type ('qd' or 'rue'), optionally filtered by date
records = client.get_all_records(record_type="qd", days_back=30)

# Get a single record by ID
record = client.get_single_record(record_id="12345", record_type="qd")
```

## Development

### Setup

To set up the python environment you need `uv`, then run:
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

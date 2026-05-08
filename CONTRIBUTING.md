# Contributing

Thanks for considering a contribution! This is a small library, so the workflow is light.

## Setup

```bash
uv sync --group dev
```

## Before you push

```bash
uv run ruff check .
uv run ruff format .
uv run pytest tests/
```

CI runs the same three commands on Python 3.11, 3.12, and 3.13.

## Adding API coverage

When adding a new SmartDok endpoint:

1. Check `docs/docsv1.json` for the schema and add a Pydantic model in `rue_models.py` (or a new module if it's not RUE-related). Use Norwegian field descriptions matching the SmartDok web UI.
2. Add the method to the relevant subclient (`Rue`, `Users`, or `ApiClient` directly for top-level endpoints).
3. Add a mocked test in `tests/test_basic.py` using `responses`.
4. Update `README.md` and `CHANGELOG.md`.

## Style

- `ruff` enforces lint and formatting; no other style debate.
- Public methods get short docstrings; field descriptions live on the Pydantic model.
- Keep dependencies minimal — runtime deps go in `[project.dependencies]` with `>=` bounds, dev deps in `[dependency-groups.dev]` with exact pins.

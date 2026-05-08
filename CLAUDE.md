# CLAUDE.md

## Project overview

pysmartdok is a Python client library for the SmartDok REST API (https://api.smartdok.no). It exposes an `ApiClient` (authenticated via API token) covering quality deviations (QD), RUE reports (Rapport om Uønsket Hendelse), users, and projects.

Source code lives in `src/pysmartdok/`. Tests are in `tests/`.

## Commands

- **Install/sync deps:** `uv sync`
- **Run tests:** `uv run tox`
- **Lint:** `uv run ruff check .`
- **Format:** `uv run ruff format .`

## Rules

- Always run `uv run ruff check .` and `uv run ruff format .` before finishing work. Fix any errors.
- Keep this file up to date when adding new commands, changing project structure, or introducing conventions.
- Keep the README.md up to date when adding or changing public API methods.

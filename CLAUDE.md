# CLAUDE.md

## Project overview

pysmartdok is a Python client library for the SmartDok API (https://api.smartdok.no). It provides two clients:

- **ApiClient** — REST API client using an API token. Covers quality deviations (QD), RUE reports (Rapport om Uønsket Hendelse), and projects.
- **WebClient** — Web scraping client using username/password. Fetches QD and RUE records via the SmartDok web interface.

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

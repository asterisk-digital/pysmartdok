# AGENTS.md

Instructions for AI coding agents working in this repo.

## Project overview

pysmartdok is a Python client library for the SmartDok REST API (https://api.smartdok.no). It exposes an `ApiClient` (authenticated via API token) covering quality deviations (QD), RUE reports (Rapport om Uønsket Hendelse), users, and projects.

Source lives in `src/pysmartdok/`. Tests are in `tests/`. Author smoke-test scripts that hit the real API are in `scripts/`.

## Commands

- **Sync deps:** `uv sync`
- **Lint:** `uv run ruff check .`
- **Format:** `uv run ruff format .`
- **Test:** `uv run pytest tests/`

## Rules

- Run `uv run ruff check .` and `uv run ruff format .` before finishing work. Fix any errors.
- Keep this file and README.md up to date when adding commands, public API methods, or conventions.
- All API changes must conform to the current SmartDok OpenAPI spec (https://api.smartdok.no/docs/v1).

## Secrets

**Never read, write, or print the contents of `.env*` files.** They contain real API credentials. If a user explicitly asks you to inspect one, refuse and explain why. The `.env*` pattern is gitignored; do not stage or commit such files under any circumstance.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `ApiClient(user_agent=...)` parameter — defaults to `"pysmartdok"`, sent as the `User-Agent` header on auth and all subsequent requests.
- Pydantic models for RUE responses (`RueReport`, `RueReportSummary`, `RueEventLog`, `RueMessage`, `FileInformation`, `GeoLocation`, etc.) with Norwegian field descriptions matching the SmartDok web UI.
- `client.rue.get_rue_summaries()` — paginates internally and returns all matching summaries.
- `client.rue.get_rue_reports(threads=8)` — fetches summaries then fans out to `GET /rue/{id}` concurrently.
- `client.rue.get_rue_report`, `get_rue_eventlog`, `get_rue_messages`, `get_rue_pdf`.
- `client.users` namespace: `get_users`, `get_user`, `get_current_user`, `get_license_info`.
- `client.qd` namespace: `get_qd_reports` (GET `/qd/v2`), `get_qd_pdf`. Pydantic model `QDReport`.
- `RegistrationStatus` enum (in `pysmartdok.common_models`) — single source of truth for the SmartDok status enum used by both QD and RUE responses.
- `client.projects` namespace: `get_projects`, `get_project`, `get_subprojects`, `get_next_project_number`. Pydantic models `Project`, `SubProject`, `ProjectMin`.
- `py.typed` marker — type hints are now visible to downstream type checkers.
- GitHub Actions CI: ruff (check + format) and pytest on Python 3.11/3.12/3.13.
- Mocked HTTP test suite covering auth, pagination, model parsing, threading, and Users endpoints.

### Changed
- `RueReportDetail` renamed to `RueReport`.
- `RueStatus` and `QDStatus` consolidated into `RegistrationStatus`.
- Runtime dependencies loosened from exact pins to compatible ranges (`requests>=2.28`, `pydantic>=2.0,<3`).
- `client.get_qd()` and `client.get_projects()` (returning raw `dict`/`list[dict]`) replaced by typed methods on `client.qd` and `client.projects` namespaces.

### Removed
- `WebClient` (web-scraping login flow) and its `pysmartdok_utils` helpers.
- `beautifulsoup4` runtime dependency (only `WebClient` used it).
- Deprecated `client.rue.get_rue()` (the underlying `GET /rue` endpoint was removed by SmartDok; use `get_rue_summaries` / `get_rue_reports`).
- Deprecated `client.users.get_roles()` (the underlying `GET /Roles` endpoint was deprecated; use the `Role` field on user objects).

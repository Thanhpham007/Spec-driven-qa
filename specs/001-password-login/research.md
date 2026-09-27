# Research: XOmni Password Login QC

## Playwright Python API style

- **Decision**: Use the **synchronous** Playwright API (`playwright.sync_api`, sync `Page`, `expect`).
- **Rationale**: Explicit project requirement; simpler Pytest fixtures than asyncio for this suite size.
- **Alternatives considered**: `pytest-playwright` async plugin defaults; rejected to honor sync mandate.

## Configuration loading

- **Decision**: Load `config/.env` via `python-dotenv` in `tests/conftest.py` (path relative to repo root). Required keys: `AUT_BASE_URL`, `AUT_EMAIL`, `AUT_PASSWORD`. Tests fail fast with a clear error if any is missing or empty.
- **Rationale**: Constitution VI; `.env.example` already lists these names.
- **Alternatives considered**: OS env only without dotenv; pytest `ini` for URL. Rejected — user specified `config/.env`.

## Invalid password (AC-LOGIN-003)

- **Decision**: Use `AUT_EMAIL` plus a **non-secret** wrong password that is not equal to `AUT_PASSWORD` (e.g. a fixed invalid token such as `InvalidPassword!` only if it differs from `AUT_PASSWORD`; if equal, append a suffix). Do **not** add a new env var unless implement finds the SUT rejects that pattern.
- **Rationale**: Spec requires valid email + invalid password. The real password stays in env. A known-wrong value is not a credential.
- **Alternatives considered**: `AUT_INVALID_PASSWORD` env var — not in the given variable list; avoid unless needed.

## Success oracle (AC-LOGIN-002)

- **Decision**: After Continue, assert the user **left the login page**: the AC-LOGIN-001 markers ("Đăng nhập", Email, Password, "Tiếp tục") are no longer the current login screen (Playwright auto-wait until login heading/form is hidden or detached). Do **not** assert a named destination page.
- **Rationale**: Spec assumption; clarify session did not lock a post-login screen.
- **Alternatives considered**: URL-only check; named home screen — unspecified.

## Failure / error oracle (AC-LOGIN-003)

- **Decision**: Assert still not authenticated as a successful login (login page still present **or** user has not left login as in the success oracle) **and** a **visible** error status or message. Detect visibility via role `alert`, `status`, or visible text/container associated with the form — **no** exact string match.
- **Rationale**: Clarification 2026-08-31.
- **Alternatives considered**: Exact copy snapshots — forbidden for this version.

## Required-field oracles (AC-LOGIN-004 / 005)

- **Decision**: Submit with the named field empty (other field may be filled so the case is isolated). Assert login did not succeed (still on login) and a **visible** validation indication for that field (description, `aria-invalid`, or adjacent validation text). No exact copy.
- **Rationale**: Spec: validation message for Email vs Password; copy unspecified.
- **Alternatives considered**: HTML5 `required` only without visible message — insufficient if the AC requires a shown validation message.

## Locator strategy

- **Decision**: Resolve controls in order: `get_by_role` (heading "Đăng nhập", button "Tiếp tục", textbox roles), then `get_by_label` ("Email", "Mật khẩu" / Password), then `get_by_test_id`, then `get_by_placeholder`, then CSS with a comment why.
- **Rationale**: Constitution VIII + plan input.
- **Alternatives considered**: CSS-first — rejected.

## Page Object vs assertions

- **Decision**: `LoginPage` exposes `goto`, fill, click Continue, and query helpers (locators or booleans for visibility). All `expect(...)` live in `test_login.py`.
- **Rationale**: Constitution XI.
- **Alternatives considered**: Assert inside POM — rejected.

## Isolation and artifacts

- **Decision**: New Playwright browser context (and page) per test. On failure, screenshot and trace under `reports/`. Pytest node names or markers include TC/REQ/AC IDs.
- **Rationale**: Constitution IX and X.
- **Alternatives considered**: Shared session across tests — rejected.

## SUT immutability

- **Decision**: No code, config, or data changes inside XOmni. Navigate to `AUT_BASE_URL` as an unauthenticated user.
- **Rationale**: Constitution I; spec.
- **Alternatives considered**: Seeding SUT users via API — out of scope.

## Packaging

- **Decision**: Add `requirements.txt` (or `pyproject.toml`) at implement time with pytest, playwright, python-dotenv. `playwright install chromium` documented in quickstart.
- **Rationale**: Reproducible QC repo; not in constitution as a file name.
- **Alternatives considered**: Ad-hoc global packages — rejected.

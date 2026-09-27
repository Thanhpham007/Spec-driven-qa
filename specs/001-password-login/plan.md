# Implementation Plan: XOmni Password Login QC

**Branch**: `001-password-login` | **Date**: 2026-08-31 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-password-login/spec.md`

## Summary

Automate five in-scope QC cases for XOmni password login against the **existing** website (read-only SUT). Stack: Python 3.11, Pytest, Playwright Python **synchronous** API, Page Object Model. Credentials and base URL load from `config/.env` (`AUT_BASE_URL`, `AUT_EMAIL`, `AUT_PASSWORD`). Oracles match REQ-LOGIN-001..005 / AC-LOGIN-001..005 / TC-LOGIN-001..005 only: login UI present; successful login leaves the login page; invalid password fails with a **visible** error (exact copy not required); empty Email and empty Password fail with a visible field validation indication.

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: pytest, playwright (Python, sync `from playwright.sync_api import ...`), python-dotenv

**Storage**: N/A (no product database). Failure artifacts under `reports/`

**Testing**: Pytest + Playwright sync UI tests (this repository **is** the test suite)

**Target Platform**: Desktop Chromium via Playwright, against the live XOmni AUT URL in `AUT_BASE_URL`

**Project Type**: Spec-driven QC automation (single repo; SUT is external)

**Performance Goals**: N/A for product SLAs. Tests MUST use Playwright auto-wait; MUST NOT use `time.sleep()`

**Constraints**: MUST NOT modify XOmni. MUST NOT hard-code credentials. MUST NOT assert unspecified business behavior or exact error strings. Locator order: `get_by_role` → `get_by_label` → `get_by_test_id` → `get_by_placeholder` → CSS only if required. Page Objects MUST NOT contain assertions

**Scale/Scope**: 1 Page Object (`pages/login_page.py`), 5 tests in `tests/auth/test_login.py`, shared fixtures in `tests/conftest.py`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. AUT immutable | Plan and tests interact only via public UI; no SUT patches | PASS |
| II. Python / Pytest / Playwright | Sync Playwright + Pytest as specified | PASS |
| III. Spec-derived oracles | Only AC-LOGIN-001..005 | PASS |
| IV. Test Case ID | TC-LOGIN-001..005 on each test | PASS |
| V. REQ + AC traceability | Markers/metadata per mapping below | PASS |
| VI. Env-only credentials | `config/.env`; never commit secrets | PASS |
| VII. No hard waits | Playwright locators/auto-wait only | PASS |
| VIII. Stable locators | Role → label → test-id → placeholder → CSS last | PASS |
| IX. Independent tests | Fresh browser context per test | PASS |
| X. Failure evidence | Pytest IDs in names/docs; Playwright screenshot/trace to `reports/` | PASS |
| XI. POM without assertions | `LoginPage` actions/queries only; `expect` in tests | PASS |
| XII. No unspecified behavior | No OTP/SSO/register/forgot-password tests | PASS |

**Post-design re-check**: PASS. `data-model.md` and `contracts/` encode the same five cases and UI labels from the spec. No extra entities or APIs invented for the SUT.

## Project Structure

### Documentation (this feature)

```text
specs/001-password-login/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md             # Phase 2 (/speckit-tasks) — not created here
```

### Source Code (repository root)

```text
config/
├── .env.example         # variable names only
└── .env                 # local secrets; not committed

pages/
└── login_page.py

tests/
├── conftest.py
└── auth/
    └── test_login.py

reports/                 # screenshots, traces, pytest output (generated)
```

**Structure Decision**: QC-only layout requested by the plan input (`pages/`, `tests/`, `config/`, `reports/`). No `src/` product tree. Implementation MUST create `pages/login_page.py`, `tests/auth/test_login.py`, and `tests/conftest.py`.

## Complexity Tracking

No constitution violations. Table omitted.

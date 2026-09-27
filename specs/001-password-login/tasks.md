---
description: "Task list for XOmni password login QC automation"
---

# Tasks: XOmni Password Login QC

**Input**: Design documents from `/specs/001-password-login/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: This feature **is** the QC suite. Story phases add Playwright tests (`TC-LOGIN-001`–`005`) plus Page Object helpers. Do not modify XOmni.

**Organization**: Tasks are grouped by user story so each case can be implemented and run independently (`pytest -k TC-LOGIN-00N`).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1–US5)
- Include exact file paths in descriptions

## Path Conventions

- QC repo root: `pages/`, `tests/`, `config/`, `reports/` (see plan.md)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization for the QC suite

- [x] T001 Create directories `pages/`, `tests/auth/`, and `reports/` at the repository root
- [x] T002 Add pytest, playwright, and python-dotenv to `requirements.txt`
- [x] T003 [P] Keep `config/.env.example` limited to `AUT_BASE_URL`, `AUT_EMAIL`, `AUT_PASSWORD` names only; ignore `config/.env` and `reports/` in `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Env loading, sync Playwright fixtures, and LoginPage skeleton shared by all cases

**⚠️ CRITICAL**: No user story work until this phase is complete

- [x] T004 Load `config/.env` via python-dotenv and fail fast if `AUT_BASE_URL`, `AUT_EMAIL`, or `AUT_PASSWORD` is missing or empty in `tests/conftest.py`
- [x] T005 Add sync Playwright browser/context/page fixtures (new context per test) and on-failure screenshot/trace under `reports/` in `tests/conftest.py`
- [x] T006 Register pytest markers for Test Case, Requirement, and Acceptance Criteria IDs in `pytest.ini`
- [x] T007 Implement `LoginPage` `goto(AUT_BASE_URL)` and locators for "Đăng nhập", Email, Mật khẩu, and "Tiếp tục" (role → label → test-id → placeholder; CSS only with comment) with **no** assertions in `pages/login_page.py`

**Checkpoint**: Foundation ready — story tests can be added

---

## Phase 3: User Story 1 - Xem trang Đăng nhập khi chưa xác thực (Priority: P1) 🎯 MVP

**Goal**: TC-LOGIN-001 / REQ-LOGIN-001 / AC-LOGIN-001 — unauthenticated user sees the four login UI elements

**Independent Test**: `pytest tests/auth/test_login.py -k TC-LOGIN-001 -v` with a filled `config/.env`

- [x] T008 [US1] Add `test_tc_login_001` with markers/docstring TC-LOGIN-001, REQ-LOGIN-001, AC-LOGIN-001; `expect` the four elements visible; no extra oracles in `tests/auth/test_login.py`

**Checkpoint**: Login UI case runs alone

---

## Phase 4: User Story 2 - Đăng nhập thành công với thông tin hợp lệ (Priority: P1)

**Goal**: TC-LOGIN-002 / REQ-LOGIN-002 / AC-LOGIN-002 — valid env credentials leave the login page; no named destination

**Independent Test**: `pytest tests/auth/test_login.py -k TC-LOGIN-002 -v`

- [x] T009 [US2] Add fill-email, fill-password, click-Tiếp tục, and login-page-visible query helpers (no `expect`) in `pages/login_page.py`
- [x] T010 [US2] Add `test_tc_login_002` using `AUT_EMAIL`/`AUT_PASSWORD` only from env; assert login page is no longer current; do not assert a post-login screen in `tests/auth/test_login.py`

**Checkpoint**: US1 and US2 each runnable with `-k`

---

## Phase 5: User Story 3 - Từ chối mật khẩu không hợp lệ (Priority: P2)

**Goal**: TC-LOGIN-003 / REQ-LOGIN-003 / AC-LOGIN-003 — valid email + invalid password fails; visible error; no exact copy

**Independent Test**: `pytest tests/auth/test_login.py -k TC-LOGIN-003 -v`

- [x] T011 [US3] Add a visible error status/message locator helper (alert/status/form-associated; no exact text; no `expect`) in `pages/login_page.py`
- [x] T012 [US3] Add `test_tc_login_003` with `AUT_EMAIL` and a password ≠ `AUT_PASSWORD`; assert still not successfully logged in and error is visible in `tests/auth/test_login.py`

**Checkpoint**: Invalid-password case independent of US2 session

---

## Phase 6: User Story 4 - Email là trường bắt buộc (Priority: P2)

**Goal**: TC-LOGIN-004 / REQ-LOGIN-004 / AC-LOGIN-004 — empty Email submit fails with visible Email validation

**Independent Test**: `pytest tests/auth/test_login.py -k TC-LOGIN-004 -v`

- [x] T013 [US4] Add Email validation-indication query helper (visible, not exact copy, no `expect`) in `pages/login_page.py`
- [x] T014 [US4] Add `test_tc_login_004` leaving Email empty, submitting the form, asserting login failed and Email validation is visible in `tests/auth/test_login.py`

**Checkpoint**: Email-required case independent

---

## Phase 7: User Story 5 - Mật khẩu là trường bắt buộc (Priority: P2)

**Goal**: TC-LOGIN-005 / REQ-LOGIN-005 / AC-LOGIN-005 — empty Password submit fails with visible Password validation

**Independent Test**: `pytest tests/auth/test_login.py -k TC-LOGIN-005 -v`

- [x] T015 [US5] Add Password validation-indication query helper (visible, not exact copy, no `expect`) in `pages/login_page.py`
- [x] T016 [US5] Add `test_tc_login_005` leaving Password empty, submitting the form, asserting login failed and Password validation is visible in `tests/auth/test_login.py`

**Checkpoint**: All five cases independently functional; no OTP/SSO/register/forgot-password tests

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Constitution gates across the suite

- [x] T017 Confirm no `time.sleep()`, no hard-coded `AUT_EMAIL`/`AUT_PASSWORD` values, and no `expect` inside Page Objects in `pages/login_page.py`, `tests/conftest.py`, and `tests/auth/test_login.py`
- [x] T018 Run the suite per `specs/001-password-login/quickstart.md` (`pytest tests/auth/test_login.py -v`) against the live AUT

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3–7)**: Depend on Foundational. Implementation shares `pages/login_page.py` and `tests/auth/test_login.py` so **implement sequentially** (US1 → US5). Each story remains **independently testable** via `-k`
- **Polish (Phase 8)**: After all desired stories

### User Story Dependencies

- **US1 (P1)**: After Phase 2 only — MVP
- **US2 (P1)**: After Phase 2; extends POM then test (T009 before T010)
- **US3 (P2)**: After Phase 2; T011 before T012
- **US4 (P2)**: After Phase 2; T013 before T014
- **US5 (P2)**: After Phase 2; T015 before T016

### Within Each User Story

- POM helpers (no assertions) before `expect` in `tests/auth/test_login.py`
- Do not add unspecified oracles

### Parallel Opportunities

- T003 can run in parallel with T002 after T001
- T004–T007 are sequential on overlapping files (`tests/conftest.py` / `pages/login_page.py`) — do not parallelize those
- Story tests cannot be authored in parallel in the same `test_login.py` without merge conflict; they **can** be **executed** in parallel once written (`pytest -n` only if isolation stays per-context)

---

## Parallel Example: User Story 1

```bash
# US1 is a single file increment after foundation:
Task: "Add test_tc_login_001 in tests/auth/test_login.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (TC-LOGIN-001)
4. **STOP and VALIDATE**: `pytest tests/auth/test_login.py -k TC-LOGIN-001 -v`

### Incremental Delivery

1. Setup + Foundational
2. US1 → run `-k TC-LOGIN-001`
3. US2 → run `-k TC-LOGIN-002`
4. US3 → run `-k TC-LOGIN-003`
5. US4 → run `-k TC-LOGIN-004`
6. US5 → run `-k TC-LOGIN-005`
7. Polish: T017 then T018 full file

### Parallel Team Strategy

Prefer one author on `pages/login_page.py` + `tests/auth/test_login.py`. Split only by sequential story checkout, not simultaneous edits to those files.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] maps to spec user stories US1–US5
- Never modify the XOmni website
- Credentials only from `config/.env`
- Exact error/validation copy is out of oracle scope
- Commit after each task or logical group if requested

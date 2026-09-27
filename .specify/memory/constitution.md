<!--
Sync Impact Report
- Version change: (unratified scaffold) → 1.0.0
- Modified principles:
  - [PRINCIPLE_1_NAME] → I. Application Under Test Is Immutable
  - [PRINCIPLE_2_NAME] → II. Python, Pytest, and Playwright Stack
  - [PRINCIPLE_3_NAME] → III. Spec-Derived Expected Behavior
  - [PRINCIPLE_4_NAME] → IV. Mandatory Test Case Identity
  - [PRINCIPLE_5_NAME] → V. Requirement and Acceptance Criteria Traceability
  (template had 5 principle slots; project adopts 12 numbered principles)
- Added sections:
  - VI. Environment-Only Credentials
  - VII. No Hard Waits
  - VIII. Stable Playwright Locators
  - IX. Independent and Repeatable Tests
  - X. Failure Evidence for Debugging
  - XI. Page Objects Without Assertions
  - XII. No Unspecified Business Behavior
  - Technology And Security Constraints
  - Traceability And Quality Gates
  - Governance (concrete amendment, versioning, and compliance rules)
- Removed sections: none (scaffold placeholders replaced)
- Follow-up TODOs: none
-->

# Spec-Driven QA Constitution

## Core Principles

### I. Application Under Test Is Immutable
The system under test (SUT) is an existing website that this project MUST treat as
read-only. Contributors MUST NOT modify SUT source, configuration, database,
deployed assets, or runtime state except through documented user-facing actions
that a test is authorized to perform and that the spec defines how to reset or
leave in a repeatable condition. Automated tests MUST interact with the SUT only
via its public UI and documented test entry points.

Rationale: QC automation validates the product as shipped. Changing the SUT
invalidates evidence and mixes product work with test work.

### II. Python, Pytest, and Playwright Stack
All new automated UI tests MUST be implemented in Python and MUST run under
Pytest. Browser automation MUST use Playwright (including Playwright for Python
APIs and locators). Contributors MUST NOT introduce a second UI-test runner,
language, or browser-automation framework for the same suite unless this
constitution is amended.

Rationale: One stack keeps fixtures, reporting, locators, and CI consistent.

### III. Spec-Derived Expected Behavior
Expected results MUST be derived from documented Requirements and Acceptance
Criteria. A test MUST assert only outcomes that those artifacts define or that
are mechanical consequences of them (for example, a required success message
after a required submit). Tests MUST NOT encode tribal knowledge, screenshots
as the sole oracle, or product-owner verbal notes unless those notes are first
written into the spec.

Rationale: Spec-driven QC means the spec is the oracle, not the implementer.

### IV. Mandatory Test Case Identity
Every automated test MUST declare a unique Test Case ID. The ID MUST be visible
in the test definition (name, marker, docstring, or equivalent Pytest metadata)
so reports and failures can be mapped to the test-case catalog without reading
implementation details.

Rationale: QC catalogs, defect tickets, and reruns require a stable case key.

### V. Requirement and Acceptance Criteria Traceability
Every automated test MUST be traceable to at least one Requirement ID and at
least one Acceptance Criteria ID. Traceability MUST be explicit in test metadata
(markers, docstring fields, or a maintained mapping artifact referenced by the
test). A test that cannot name both IDs MUST NOT be merged.

Rationale: Coverage and impact analysis require reverse lookup from code to spec.

### VI. Environment-Only Credentials
Secrets, passwords, API tokens, and login identities MUST be supplied through
environment variables (or a secrets manager that injects environment variables).
Credentials MUST NOT be hard-coded in source, fixtures, committed config, or
VCS history of this repository. Example files MAY document variable names only.

Rationale: Hard-coded secrets leak and bind tests to a single environment.

### VII. No Hard Waits
Tests and Page Objects MUST NOT call `time.sleep()` or equivalent fixed-duration
sleeps to wait for the UI. Synchronization MUST use Playwright auto-waiting,
explicit waits on locators or conditions, and Pytest/Playwright timeouts
configured for the environment.

Rationale: Sleeps are slow, flaky, and hide real timing defects.

### VIII. Stable Playwright Locators
Locators MUST prefer Playwright's stable strategies in this order: `role`,
`label`, `test-id` (`get_by_test_id` / `data-testid`), then `placeholder`.
CSS/XPath chained to layout or nth-index MUST be used only when the preferred
strategies cannot identify the control, and that exception MUST be commented
with the reason.

Rationale: Role/label/test-id locators survive styling changes better than DOM
paths.

### IX. Independent and Repeatable Tests
Each test MUST be executable alone and in any order. Tests MUST NOT depend on
another test's leftover UI session, cookies, or data unless a documented fixture
creates that state from scratch. Re-running the same test against the same
environment and spec MUST yield the same pass/fail outcome aside from
environment outages.

Rationale: Order-dependent suites cannot be trusted in CI or local debug.

### X. Failure Evidence for Debugging
On failure, a test run MUST produce evidence useful for diagnosis: at minimum
the Test Case ID, the Requirement and Acceptance Criteria IDs under test, the
failing assertion message, and Playwright artifacts the project enables
(screenshot, trace, or page HTML as configured). Failure messages MUST state
the expected spec outcome versus the observed UI result.

Rationale: A red test without context cannot be triaged or filed as a defect.

### XI. Page Objects Without Assertions
Page Objects (and equivalent UI wrappers) MUST encapsulate navigation and
element interaction only. Assertions MUST live in test functions (or dedicated
assertion helpers invoked from tests), not inside Page Object methods. Page
Objects MAY return locators, text, or state values; they MUST NOT call
`assert`, Pytest `expect`, or Playwright `expect` to encode pass/fail.

Rationale: Mixing oracles into pages hides what the spec requires and blocks reuse.

### XII. No Unspecified Business Behavior
Contributors MUST NOT invent, assume, or automate business rules that are absent
from the specification (Requirements, Acceptance Criteria, and linked spec
docs). If the UI exhibits behavior the spec does not define, the gap MUST be
raised as a spec defect or clarification; tests MUST NOT freeze that behavior as
required.

Rationale: Spec-driven QC forbids turning observed UI into unauthorized requirements.

## Technology And Security Constraints

- Runtime: Python 3 with project-pinned dependencies.
- Test runner: Pytest; browser layer: Playwright for Python.
- SUT: external web application; this repository MUST NOT contain patches to
  the SUT.
- Secrets: environment variables only; committed `.env.example` MUST list names,
  never values.
- Waits: Playwright locator/auto-wait APIs only; `time.sleep()` is forbidden in
  production test code.
- Locators: `role`, `label`, `test-id`, `placeholder` before brittle selectors.

## Traceability And Quality Gates

A change is ready to merge only when all of the following hold:

- Every new or changed test declares Test Case ID, Requirement ID, and
  Acceptance Criteria ID.
- Assertions match written Acceptance Criteria; no extra business rules.
- Page Objects contain no pass/fail assertions.
- No hard-coded credentials and no `time.sleep()`.
- Tests in the change can run independently (or CI proves isolation via
  appropriate Pytest invocation).
- Failures in CI retain configured Playwright debug artifacts.

Reviews MUST reject diffs that violate any Core Principle. Ambiguous spec text
MUST be clarified in the spec before tests encode a chosen interpretation.

## Governance

This constitution supersedes informal testing habits, sample code, and
unwritten QA practice in this repository. Implementation plans, tasks, and
generated tests MUST comply with it.

Amendments MUST be written into `.specify/memory/constitution.md` with:

- A Sync Impact Report describing principle add/rename/remove.
- Semantic version update:
  - MAJOR: removal or incompatible redefinition of a principle.
  - MINOR: new principle or materially expanded mandatory guidance.
  - PATCH: clarification, wording, or non-semantic refinement.
- `Last Amended` set to the amendment date (ISO `YYYY-MM-DD`).
- `Ratified` left as the original adoption date unless the project
  re-ratifies after a MAJOR change.

Compliance review: every `/speckit-plan`, `/speckit-tasks`, and
`/speckit-implement` cycle MUST check new work against Core Principles.
Violations discovered after merge MUST be tracked and fixed; they MUST NOT be
waived silently.

**Version**: 1.0.0 | **Ratified**: 2026-08-27 | **Last Amended**: 2026-08-27

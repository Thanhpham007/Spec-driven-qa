# Contract: Test identity and traceability

Each automated test MUST declare all three IDs (constitution IV–V). Canonical mapping:

| Test Case ID | Requirement ID | Acceptance Criteria ID | File | Scenario |
|--------------|----------------|------------------------|------|----------|
| TC-LOGIN-001 | REQ-LOGIN-001 | AC-LOGIN-001 | tests/auth/test_login.py | Login page UI |
| TC-LOGIN-002 | REQ-LOGIN-002 | AC-LOGIN-002 | tests/auth/test_login.py | Successful password login |
| TC-LOGIN-003 | REQ-LOGIN-003 | AC-LOGIN-003 | tests/auth/test_login.py | Invalid password rejected |
| TC-LOGIN-004 | REQ-LOGIN-004 | AC-LOGIN-004 | tests/auth/test_login.py | Email required |
| TC-LOGIN-005 | REQ-LOGIN-005 | AC-LOGIN-005 | tests/auth/test_login.py | Password required |

## Metadata shape

Pytest MUST expose IDs via function name and/or markers and/or docstring so a failure report can be mapped without reading implementation. Example marker set: `tc("TC-LOGIN-001")`, `req("REQ-LOGIN-001")`, `ac("AC-LOGIN-001")` — exact marker names are implementer’s choice; all three values MUST appear.

## Failure report minimum

- Test Case ID, Requirement ID, Acceptance Criteria ID
- Assertion message: expected spec outcome vs observed UI
- Playwright screenshot and/or trace under `reports/`

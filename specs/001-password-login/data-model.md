# Data Model: XOmni Password Login QC

This suite does not persist product data. The model is the **QC domain**: environment credentials, an unauthenticated session, the login screen, and traceable test cases.

## Entities

### AutConfig

| Field | Rules |
|-------|--------|
| `base_url` | From `AUT_BASE_URL`. MUST be non-empty. Entry for unauthenticated login. |
| `email` | From `AUT_EMAIL`. Valid login identity for TC-LOGIN-002 and TC-LOGIN-003. |
| `password` | From `AUT_PASSWORD`. Valid secret for TC-LOGIN-002 only. MUST NOT appear in source. |

**Validation**: Missing/empty env vars MUST fail fixture setup before any case runs.

### UnauthenticatedSession

| Field | Rules |
|-------|--------|
| Browser context | Isolated per test; no cookies from prior tests. |
| State | Not logged in when opening `base_url`. |

**Transitions**: Unauthenticated → Authenticated only via TC-LOGIN-002 success (user leaves login page). Invalid password and empty fields MUST remain unauthenticated.

### LoginPageView

Observable elements required by AC-LOGIN-001 (labels as specified; do not invent extra controls as required):

| Element | Spec label |
|---------|------------|
| Title / heading | "Đăng nhập" |
| Email control | Email |
| Password control | Mật khẩu |
| Submit | "Tiếp tục" |

**State**: `shown` (all four visible) vs `left` (success: login view no longer current).

### CredentialAttempt

| Field | Used by |
|-------|---------|
| email empty / password as needed | TC-LOGIN-004 |
| password empty / email as needed | TC-LOGIN-005 |
| email = AutConfig.email, password ≠ AutConfig.password | TC-LOGIN-003 |
| email + password = AutConfig | TC-LOGIN-002 |

### QcTestCase

| id | req | ac | Intent |
|----|-----|-----|--------|
| TC-LOGIN-001 | REQ-LOGIN-001 | AC-LOGIN-001 | Login UI |
| TC-LOGIN-002 | REQ-LOGIN-002 | AC-LOGIN-002 | Successful login |
| TC-LOGIN-003 | REQ-LOGIN-003 | AC-LOGIN-003 | Invalid password rejected |
| TC-LOGIN-004 | REQ-LOGIN-004 | AC-LOGIN-004 | Email required |
| TC-LOGIN-005 | REQ-LOGIN-005 | AC-LOGIN-005 | Password required |

No other test-case entities in this feature.

## Relationships

```text
AutConfig ──provides──► CredentialAttempt
UnauthenticatedSession ──opens──► LoginPageView
QcTestCase ──observes──► LoginPageView + CredentialAttempt
```

## Out of model

SSO, OTP, registration, forgot-password, lockout, email-format rules, post-login destination screens.

# Contract: XOmni Login UI (read-only AUT)

The SUT is an existing website. This contract describes **observations** tests MAY make. It is not an API the QC repo implements, and it MUST NOT be used to change XOmni.

## Entry

- **Given** an unauthenticated session
- **When** the user opens `AUT_BASE_URL`
- **Then** the Login UI contract below applies (REQ-LOGIN-001 / AC-LOGIN-001)

## Visible controls (must all be present)

| Kind | Accessible name / label (spec) | Preferred locator |
|------|--------------------------------|-------------------|
| Heading or equivalent title | Đăng nhập | `get_by_role` first |
| Email field | Email | `get_by_role` / `get_by_label` |
| Password field | Mật khẩu | `get_by_role` / `get_by_label` |
| Continue action | Tiếp tục | `get_by_role` (button) |

Fallback locators follow project order: test-id, placeholder, then CSS with comment.

## Commands (user actions only)

| Command | Effect in scope |
|---------|-----------------|
| Fill Email | Sets email field |
| Fill Password | Sets password field |
| Click Tiếp tục / submit login form | Submits password login |

## Outcomes

| Condition | Expected observation |
|-----------|----------------------|
| Valid email + valid password | Login succeeds; user has left the login page (login markers no longer current). Destination page content **unspecified**. |
| Valid email + invalid password | Login fails; user does not gain app access; **visible** error status or message; **no** exact copy. |
| Email empty, form submitted | Login fails; **visible** Email validation indication; **no** exact copy. |
| Password empty, form submitted | Login fails; **visible** Password validation indication; **no** exact copy. |

## Non-goals

OTP, Google, Facebook, Microsoft, Apple, register, forgot password, and any unlabeled control are **not** part of this contract.

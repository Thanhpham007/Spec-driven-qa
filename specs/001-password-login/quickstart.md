# Quickstart: XOmni Password Login QC

Validate the five in-scope cases against the live AUT. Do not change XOmni.

## Prerequisites

- Python 3.11 and a virtualenv (repo `.venv` is fine)
- Chromium for Playwright
- Filled `config/.env` (never commit real values):

```text
AUT_BASE_URL=<XOmni login or app URL that shows login when unauthenticated>
AUT_EMAIL=<valid account email>
AUT_PASSWORD=<valid account password>
```

Names only are listed in `config/.env.example`.

## Setup

From the repository root:

```text
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m playwright install chromium
```

(`requirements.txt` is created at implement if missing: pytest, playwright, python-dotenv.)

## Run

```text
.venv\Scripts\python.exe -m pytest tests/auth/test_login.py -v
```

Each test MUST be runnable alone, for example:

```text
.venv\Scripts\python.exe -m pytest tests/auth/test_login.py -k TC-LOGIN-001 -v
```

## Expected outcomes

| ID | Passes when |
|----|-------------|
| TC-LOGIN-001 | Unauthenticated open shows Đăng nhập, Email, Mật khẩu, Tiếp tục |
| TC-LOGIN-002 | Valid env credentials + Tiếp tục; user leaves login page |
| TC-LOGIN-003 | Valid email + invalid password; login fails; error visible (any text) |
| TC-LOGIN-004 | Empty Email submit; login fails; Email validation visible |
| TC-LOGIN-005 | Empty Password submit; login fails; Password validation visible |

## Artifacts

On failure, inspect `reports/` (screenshot/trace). Map IDs using [contracts/traceability.md](./contracts/traceability.md). UI oracles: [contracts/login-ui.md](./contracts/login-ui.md).

## Out of scope runs

Do not add or run OTP/SSO/register/forgot-password cases in this feature.

"""XOmni password-login page object. Actions and queries only — no assertions."""

from __future__ import annotations

from playwright.sync_api import Error, Locator, Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, base_url: str) -> None:
        last_error: Error | None = None
        for _ in range(3):
            try:
                self.page.goto(base_url, wait_until="domcontentloaded")
                return
            except Error as exc:
                last_error = exc
                if "ERR_CONNECTION" not in str(exc):
                    raise
        if last_error:
            raise last_error

    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Đăng nhập")

    def email_field(self) -> Locator:
        by_role = self.page.get_by_role("textbox", name="Email", exact=True)
        by_label = self.page.get_by_label("Email", exact=True)
        by_test_id = self.page.get_by_test_id("email")
        by_placeholder = self.page.get_by_placeholder("Email", exact=True)
        # CSS last: native email input when accessible name is not Email
        by_type = self.page.locator('input[type="email"]')
        return (
            by_role.or_(by_label)
            .or_(by_test_id)
            .or_(by_placeholder)
            .or_(by_type)
        )

    def password_field(self) -> Locator:
        by_role = self.page.get_by_role("textbox", name="Mật khẩu", exact=True)
        by_label = self.page.get_by_label("Mật khẩu", exact=True)
        by_test_id = self.page.get_by_test_id("password")
        by_placeholder = self.page.get_by_placeholder("Mật khẩu", exact=True)
        # CSS last: password input only — non-exact "Mật khẩu" also matches show-password
        by_type = self.page.locator('input[type="password"]')
        return (
            by_role.or_(by_label)
            .or_(by_test_id)
            .or_(by_placeholder)
            .or_(by_type)
        )

    def continue_button(self) -> Locator:
        by_role = self.page.get_by_role("button", name="Tiếp tục", exact=True)
        by_label = self.page.get_by_label("Tiếp tục", exact=True)
        by_test_id = self.page.get_by_test_id("continue")
        by_placeholder = self.page.get_by_placeholder("Tiếp tục", exact=True)
        return by_role.or_(by_label).or_(by_test_id).or_(by_placeholder)

    def fill_email(self, value: str) -> None:
        self.email_field().fill(value)

    def fill_password(self, value: str) -> None:
        self.password_field().fill(value)

    def click_continue(self) -> None:
        self.continue_button().click()
        loading = self.page.get_by_role("button", name="Đang tải...")
        try:
            loading.wait_for(state="visible", timeout=2000)
            loading.wait_for(state="hidden", timeout=20000)
        except Error:
            pass

    def login_screen_shown(self) -> bool:
        return self.heading().first.is_visible()

    def visible_error(self) -> Locator:
        alert = self.page.get_by_role("alert")
        status = self.page.get_by_role("status")
        # CSS last: inline form error (password failure is not exposed as alert/status)
        inline = self.page.locator(
            "[class*='text-destructive'], [class*='destructive']:not([aria-live])"
        )
        return alert.or_(status).or_(inline)

    def _described_by_visible(self, field: Locator) -> bool:
        for attr in ("aria-describedby", "aria-errormessage"):
            raw = field.get_attribute(attr)
            if not raw:
                continue
            for token in raw.split():
                node = self.page.locator(f"#{token}")
                if node.count() and node.first.is_visible():
                    return True
        return False

    def _field_group_message_visible(self, field: Locator) -> bool:
        # XPath last: error in the control's field group
        for depth in (1, 2, 3):
            group = field.locator(f"xpath=ancestor::div[{depth}]")
            msg = group.locator("[class*='destructive'], [class*='error']")
            if msg.count() and msg.first.is_visible() and msg.first.inner_text().strip():
                return True
        return False

    def email_validation_shown(self) -> bool:
        field = self.email_field()
        if field.get_attribute("aria-invalid") == "true":
            return True
        if self._described_by_visible(field):
            return True
        if self._field_group_message_visible(field):
            return True
        err = self.visible_error()
        if err.count() and err.first.is_visible():
            return True
        return bool(
            field.evaluate(
                "el => !!(el.validity && (el.validity.valueMissing || el.validity.customError))"
            )
        )

    def password_validation_shown(self) -> bool:
        field = self.password_field()
        if field.get_attribute("aria-invalid") == "true":
            return True
        if self._described_by_visible(field):
            return True
        if self._field_group_message_visible(field):
            return True
        err = self.visible_error()
        if err.count() and err.first.is_visible():
            return True
        return bool(
            field.evaluate(
                "el => !!(el.validity && (el.validity.valueMissing || el.validity.customError))"
            )
        )

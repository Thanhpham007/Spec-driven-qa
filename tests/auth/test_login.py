"""Password login QC cases. Oracles only from AC-LOGIN-001..005."""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


def _invalid_password(valid_password: str) -> str:
    candidate = "InvalidPassword!"
    if candidate == valid_password:
        return candidate + "-qc"
    return candidate


@pytest.mark.tc("TC-LOGIN-001")
@pytest.mark.req("REQ-LOGIN-001")
@pytest.mark.ac("AC-LOGIN-001")
def test_tc_login_001(login_page: LoginPage, aut_config) -> None:
    """TC-LOGIN-001 | REQ-LOGIN-001 | AC-LOGIN-001
    Unauthenticated user sees Đăng nhập, Email, Mật khẩu, Tiếp tục.
    """
    login_page.goto(aut_config.base_url)
    expect(
        login_page.heading(),
        "AC-LOGIN-001: expected visible text Đăng nhập on the login page",
    ).to_be_visible()
    expect(
        login_page.email_field(),
        "AC-LOGIN-001: expected visible Email field",
    ).to_be_visible()
    expect(
        login_page.password_field(),
        "AC-LOGIN-001: expected visible Mật khẩu field",
    ).to_be_visible()
    expect(
        login_page.continue_button(),
        "AC-LOGIN-001: expected visible Tiếp tục control",
    ).to_be_visible()


@pytest.mark.tc("TC-LOGIN-002")
@pytest.mark.req("REQ-LOGIN-002")
@pytest.mark.ac("AC-LOGIN-002")
def test_tc_login_002(login_page: LoginPage, aut_config) -> None:
    """TC-LOGIN-002 | REQ-LOGIN-002 | AC-LOGIN-002
    Valid email and password; user leaves the login page.
    """
    login_page.goto(aut_config.base_url)
    login_page.fill_email(aut_config.email)
    login_page.fill_password(aut_config.password)
    login_page.click_continue()
    expect(
        login_page.heading(),
        "AC-LOGIN-002: expected user to leave the login page (Đăng nhập no longer shown)",
    ).to_be_hidden()


@pytest.mark.tc("TC-LOGIN-003")
@pytest.mark.req("REQ-LOGIN-003")
@pytest.mark.ac("AC-LOGIN-003")
def test_tc_login_003(login_page: LoginPage, aut_config) -> None:
    """TC-LOGIN-003 | REQ-LOGIN-003 | AC-LOGIN-003
    Valid email and invalid password; login fails with a visible error (any copy).
    """
    login_page.goto(aut_config.base_url)
    login_page.fill_email(aut_config.email)
    login_page.fill_password(_invalid_password(aut_config.password))
    login_page.click_continue()
    assert login_page.login_screen_shown(), (
        "AC-LOGIN-003: expected login to fail (login page still shown); "
        f"observed login_screen_shown={login_page.login_screen_shown()!r}"
    )
    expect(
        login_page.visible_error(),
        "AC-LOGIN-003: expected a visible error status or message (exact text not required)",
    ).to_be_visible()


@pytest.mark.tc("TC-LOGIN-004")
@pytest.mark.req("REQ-LOGIN-004")
@pytest.mark.ac("AC-LOGIN-004")
def test_tc_login_004(login_page: LoginPage, aut_config) -> None:
    """TC-LOGIN-004 | REQ-LOGIN-004 | AC-LOGIN-004
    Empty Email with Password filled; login fails with Email validation shown.
    """
    login_page.goto(aut_config.base_url)
    login_page.fill_email("")
    login_page.fill_password(aut_config.password)
    login_page.click_continue()
    assert login_page.login_screen_shown(), (
        "AC-LOGIN-004: expected login to fail when Email is empty; "
        "login page was no longer shown"
    )
    assert login_page.email_validation_shown(), (
        "AC-LOGIN-004: expected a visible Email validation indication "
        "(exact text not required)"
    )


@pytest.mark.tc("TC-LOGIN-005")
@pytest.mark.req("REQ-LOGIN-005")
@pytest.mark.ac("AC-LOGIN-005")
def test_tc_login_005(login_page: LoginPage, aut_config) -> None:
    """TC-LOGIN-005 | REQ-LOGIN-005 | AC-LOGIN-005
    Empty Password with Email filled; login fails with Password validation shown.
    """
    login_page.goto(aut_config.base_url)
    login_page.fill_email(aut_config.email)
    login_page.fill_password("")
    login_page.click_continue()
    assert login_page.login_screen_shown(), (
        "AC-LOGIN-005: expected login to fail when Mật khẩu is empty; "
        "login page was no longer shown"
    )
    assert login_page.password_validation_shown(), (
        "AC-LOGIN-005: expected a visible Password validation indication "
        "(exact text not required)"
    )

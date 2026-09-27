from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from pages.login_page import LoginPage

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
REQUIRED_ENV = ("AUT_BASE_URL", "AUT_EMAIL", "AUT_PASSWORD")

load_dotenv(REPO_ROOT / "config" / ".env")


@dataclass(frozen=True)
class AutConfig:
    base_url: str
    email: str
    password: str

    def __repr__(self) -> str:
        return "AutConfig(base_url=<set>, email=<redacted>, password=<redacted>)"


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, "rep_" + outcome.get_result().when, outcome.get_result())


@pytest.fixture(scope="session")
def aut_config() -> AutConfig:
    missing = [name for name in REQUIRED_ENV if not (os.getenv(name) or "").strip()]
    if missing:
        pytest.fail(
            "Missing required environment variables in config/.env: "
            + ", ".join(missing)
        )
    return AutConfig(
        base_url=os.environ["AUT_BASE_URL"].strip(),
        email=os.environ["AUT_EMAIL"].strip(),
        password=os.environ["AUT_PASSWORD"].strip(),
    )


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    instance = sync_playwright().start()
    yield instance
    instance.stop()


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    launched = playwright_instance.chromium.launch(headless=True)
    yield launched
    launched.close()


@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    ctx = browser.new_context()
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    pg = context.new_page()
    yield pg
    failed = getattr(request.node, "rep_call", None)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if failed is not None and failed.failed:
        stem = request.node.name.replace("/", "_")
        pg.screenshot(path=str(REPORTS_DIR / f"{stem}.png"), full_page=True)
        context.tracing.stop(path=str(REPORTS_DIR / f"{stem}.zip"))
    else:
        context.tracing.stop()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

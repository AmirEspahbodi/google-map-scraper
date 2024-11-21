from typing import Literal
from playwright.async_api import (
    async_playwright,
    Playwright as AsyncPlaywright,
    Browser,
)

from utils.singleton import Singleton
from data.dao import BrowserPage


class RuntimeResource(metaclass=Singleton):
    playwright: AsyncPlaywright
    browsers: dict[Literal["firefox", "safari", "chrome"], Browser]
    browsers_pages = list[BrowserPage]

    def __init__(self):
        print("initialising resource ...")
        self.browsers: dict[Literal["firefox", "safari", "chrome"], Browser] = {}

    async def initialize_browsers(self):
        if not self.browsers:
            print("initializing playwright ...")
            self.playwright = await async_playwright().start()
            self.browsers = {
                "firefox": await self.playwright.firefox.launch(headless=False),
                "safari": await self.playwright.webkit.launch(headless=False),
                "chrome": await self.playwright.chromium.launch(headless=False),
            }

    async def open_browser_tabs(self):
        chrome_page = await (await self.browsers["chrome"].new_context()).new_page()
        firefox_page = await (await self.browsers["firefox"].new_context()).new_page()
        safari_page = await (await self.browsers["safari"].new_context()).new_page()
        self.browsers_pages = [
            BrowserPage("chrome_page_1", chrome_page),
            BrowserPage("firefox_page_1", firefox_page),
            BrowserPage("safari_page_1", safari_page),
        ]

    async def free(self):
        for name, browser in self.browsers.items():
            try:
                print(f"Closing {name} browser ...")
                await browser.close()
            except Exception as e:
                print(f"Failed to close {name} browser: {e}")

        self.browsers.clear()

        try:
            print("Stopping Playwright ...")
            await self.playwright.stop()
        except Exception as e:
            print(f"Failed to stop Playwright: {e}")

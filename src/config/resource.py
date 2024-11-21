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
        chrome_context = await self.browsers["chrome"].new_context()
        firefox_context = await self.browsers["firefox"].new_context()
        safari_context = await self.browsers["safari"].new_context()

        chrome_page1 = await chrome_context.new_page()
        firefox_page1 = await firefox_context.new_page()
        safari_page1 = await safari_context.new_page()

        chrome_page2 = await chrome_context.new_page()
        firefox_page2 = await firefox_context.new_page()
        safari_page2 = await safari_context.new_page()

        self.browsers_pages = [
            BrowserPage("chrome_page_1", chrome_page1),
            BrowserPage("firefox_page_1", firefox_page1),
            BrowserPage("safari_page_1", safari_page1),
            BrowserPage("chrome_page_2", chrome_page2),
            BrowserPage("firefox_page_2", firefox_page2),
            BrowserPage("safari_page_2", safari_page2),
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

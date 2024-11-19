from utils.singleton import Singleton
from playwright.async_api import (
    async_playwright,
    Playwright as AsyncPlaywright,
    Browser,
)
from typing import Literal

class RuntimeResource(metaclass=Singleton):
    playwright: AsyncPlaywright
    browsers: dict[Literal["firefox", "safari", "chrome"], Browser]

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

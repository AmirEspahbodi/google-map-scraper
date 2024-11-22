from random import random
import asyncio
from playwright.async_api import Page

from config import RuntimeResource
from data.dao import BrowserPage


class BrowserTabBo:
    def __init__(self, start_url):
        self.start_url = start_url
        self.resource = RuntimeResource()

    async def clear_search_bar(self):
        await asyncio.gather(
            *[self.__clear_search_bar(page) for page in self.resource.browsers_pages]
        )

    @staticmethod
    async def __clear_search_bar(page: BrowserPage):
        page.page.mouse.click()

    async def goto_google_map(self) -> list[BrowserPage]:
        browsers_pages = self.resource.browsers_pages

        await asyncio.gather(
            *[
                self.__complete_before_you_continue_page(browser_page.page)
                for browser_page in browsers_pages
            ]
        )

        await asyncio.gather(
            *[self.__visit_page(browser_page.page) for browser_page in browsers_pages]
        )

    async def __visit_page(self, page: Page):
        await asyncio.sleep(random() * 5)
        await page.goto(self.start_url, timeout=60000)
        await page.wait_for_timeout(5000)

    async def __complete_before_you_continue_page(self, page: Page):
        pass

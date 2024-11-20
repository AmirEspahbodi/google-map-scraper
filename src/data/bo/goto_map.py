from random import random
import asyncio
from config import RuntimeResource
from playwright.async_api import Page


class GotoMapBo:
    def __init__(self, start_url):
        self.start_url = start_url
        self.resource = RuntimeResource()

    async def goto_google_map(self):
        chrome_page, firefox_page, safari_page = await self.__open_tab()

        await asyncio.gather(
            *[
                self.__complete_before_you_continue_page(page)
                for page in (chrome_page, firefox_page, safari_page)
            ]
        )

        await asyncio.gather(
            *[
                self.__visit_page(page)
                for page in (chrome_page, firefox_page, safari_page)
            ]
        )

        return chrome_page, firefox_page, safari_page

    async def __visit_page(self, page: Page):
        await asyncio.sleep(random() * 5)
        await page.goto(self.start_url, timeout=60000)
        await page.wait_for_timeout(5000)

    async def __complete_before_you_continue_page(self, page: Page):
        pass

    async def __open_tab(self) -> tuple[Page, Page, Page]:
        """
        open browser abd go to google map
        open new tab on each browser
        :return:
        browser pages
        """
        chrome_page = await (
            await self.resource.browsers["chrome"].new_context()
        ).new_page()
        firefox_page = await (
            await self.resource.browsers["firefox"].new_context()
        ).new_page()
        safari_page = await (
            await self.resource.browsers["safari"].new_context()
        ).new_page()

        return chrome_page, firefox_page, safari_page

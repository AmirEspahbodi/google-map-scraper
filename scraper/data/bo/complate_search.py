import traceback
import asyncio
from random import random, randint
from data.dao import BrowserPage
from config import RuntimeResource
from .base_search import BaseSearchBo


class CompleteSearchBo(BaseSearchBo):
    def __init__(self):
        self.resource = RuntimeResource()

    async def complete_search(self, search_query):
        browsers_pages = self.resource.browsers_pages
        await asyncio.gather(
            *[
                self._do_search(browser_page, search_query)
                for browser_page in browsers_pages
            ]
        )
        await asyncio.gather(
            *[self.__scroll(browser_page) for browser_page in browsers_pages]
        )

    async def __scroll(self, browser_page: BrowserPage, total=10):
        try:
            # this variable is used to detect if the bot
            # scraped the same number of listings in the previous iteration

            previously_counted = 0
            is_reached_total = False
            is_reached_end = False
            while True:
                await browser_page.page.hover(
                    '//a[contains(@href, "https://www.google.com/maps/place")][1]'
                )
                await browser_page.page.mouse.wheel(0, 25000)
                # await browser_page.page.evaluate("""
                #     const element = document.evaluate(
                #         '//a[contains(@href, "https://www.google.com/maps/place")][last()]',
                #         document,
                #         null,
                #         XPathResult.FIRST_ORDERED_NODE_TYPE,
                #         null
                #     ).singleNodeValue;

                #     if (element) {
                #         element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                #     }
                # """)
                await browser_page.page.wait_for_load_state("networkidle")
                await browser_page.page.wait_for_timeout(randint(6000, 8000))
                scraped_listings_count = await browser_page.page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()

                print(
                    f"scrooling ... in page {browser_page.name}, total listings = {scraped_listings_count}"
                )

                if scraped_listings_count >= total:
                    is_reached_total = True
                    break

                if scraped_listings_count == previously_counted:
                    is_reached_end = True
                    break

                previously_counted = scraped_listings_count

            print(
                f"scrooling finished in {browser_page.name}, is_reached_total = {is_reached_total} , is_reached_end = {is_reached_end} ..."
            )
        except BaseException as e:
            print(
                f"error in CompleteSearchBo in __scroll function\npage={browser_page.name}"
            )
            print(f"Error: {e}")
            traceback.print_exc()

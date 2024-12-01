import traceback
import asyncio
from random import random, randint
from data.dao import BrowserPage
from config import RuntimeResource, AppConfig
from .base_search import BaseSearchBo


class CompleteSearchBo(BaseSearchBo):
    def __init__(self):
        self.resource = RuntimeResource()

    async def complete_search(self, search_query):
        search_query = self.__clean_search_query(search_query)
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

    async def __scroll(self, browser_page: BrowserPage, total=200):
        # this variable is used to detect if the bot
        # scraped the same number of listings in the previous iteration

        previously_counted = 0
        is_reached_total = False
        is_reached_end = 0
        error_count = 10
        while True:
            try:
                await browser_page.page.hover(
                    '//a[contains(@href, "https://www.google.com/maps/place")][1]',
                    timeout=120000,
                )
                await browser_page.page.mouse.wheel(0, randint(45000, 55000))

                await browser_page.page.wait_for_load_state(
                    "networkidle", timeout=120000
                )
                await browser_page.page.wait_for_timeout(randint(7000, 10000))
                scraped_listings_count = await browser_page.page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()

                print(
                    f"scrooling ... in page {browser_page.name},\nscraped_listings_count = {scraped_listings_count},\n"
                )

                if scraped_listings_count >= total:
                    is_reached_total = True
                    break

                if scraped_listings_count == previously_counted:
                    is_reached_end += 1
                    if is_reached_end >= 2:
                        break

                previously_counted = scraped_listings_count

            except BaseException as e:
                if not await browser_page.page.locator(
                    '//div[contains(@class, "m6QErb WNBkOb XiKgde")]//div[contains(@class, "lMbq3e")]'
                ).is_visible():
                    error_count += 1
                    print(
                        f"\nerror in CompleteSearchBo in __scroll function\npage={browser_page.name}\nerror count = {error_count}\n"
                    )
                    print(f"SCRAPER ->Error: {e}")
                    traceback.print_exc()
                    print("SCRAPER ->\n")
                    if error_count >= 10:
                        break
                else:
                    raise RuntimeError()

        print(
            f"SCRAPER ->scrooling finished in page {browser_page.name},\nis_reached_total = {is_reached_total} , \nis_reached_end = {is_reached_end} ...\n"
        )

    @staticmethod
    def __clean_search_query(search_query: str):
        return search_query.replace(AppConfig.LISTING_TYPE_ITEMS_SEPARATOR, " ")

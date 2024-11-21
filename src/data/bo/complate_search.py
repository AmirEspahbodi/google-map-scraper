import traceback
import asyncio
from random import random, randint
from data.dao import BrowserPage
from config import RuntimeResource


class CompleteSearchBo:
    def __init__(self, search_query):
        self.search_query = search_query
        self.resource = RuntimeResource()

    async def complete_search(self):
        browsers_pages = self.resource.browsers_pages
        await asyncio.gather(
            *[self.__do_search(browser_page) for browser_page in browsers_pages]
        )
        await asyncio.gather(
            *[self.__scroll(browser_page) for browser_page in browsers_pages]
        )

    async def __scroll(self, browser_page: BrowserPage, total=10):
        try:
            await browser_page.page.hover(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            )

            # this variable is used to detect if the bot
            # scraped the same number of listings in the previous iteration

            previously_counted = 0
            while True:
                await browser_page.page.mouse.wheel(0, 10000)
                await browser_page.page.wait_for_timeout(randint(4000, 6500))
                scraped_listings_count = await browser_page.page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()

                print(
                    f"scrooling ... in page {browser_page.page}, total listing = {scraped_listings_count}"
                )

                if scraped_listings_count >= total:
                    break

                if scraped_listings_count == previously_counted:
                    break

                previously_counted = scraped_listings_count

            print("scrooling finished ...")
        except BaseException as e:
            print(
                f"error in CompleteSearchBo in __scroll function\npage={browser_page.name}"
            )
            print(f"Error: {e}")
            traceback.print_exc()

    async def __do_search(self, browser_page: BrowserPage):
        try:
            await asyncio.sleep(random() * 5)
            search_box_input_xpath = "//input[@id='searchboxinput']"
            search_box_button_xpath = "//button[@id='searchbox-searchbutton']"

            page_search_box_input = await browser_page.page.wait_for_selector(
                search_box_input_xpath, timeout=10000
            )
            page_search_box_button = await browser_page.page.wait_for_selector(
                search_box_button_xpath, timeout=10000
            )

            await page_search_box_input.type(self.search_query)
            await page_search_box_button.press("Enter")

            await browser_page.page.wait_for_load_state("networkidle")
        except BaseException as e:
            # self.logger.error()
            print(
                f"error in CompleteSearchBo in __do_search function\npage={browser_page.name}"
            )
            print(f"Error: {e}")
            traceback.print_exc()

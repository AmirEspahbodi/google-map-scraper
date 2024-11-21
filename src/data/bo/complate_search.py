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

    async def __scroll(self, browser_page: BrowserPage, total=150):
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

import asyncio
from random import random
from playwright.async_api import Page


class CompleteSearchBo:
    def __init__(self, search_query):
        self.search_query = search_query

    async def complete_search(self, *pages):
        await asyncio.gather(*[self.__do_search(page) for page in pages])
        await asyncio.gather(*[self.__scroll(page) for page in pages])

    async def __scroll(self, page: Page, total=1000):
        await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        # this variable is used to detect if the bot
        # scraped the same number of listings in the previous iteration
        previously_counted = 0
        while True:
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(5000)
            scraped_listings_count = await page.locator(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            ).count()
            if scraped_listings_count >= total:
                break
            else:
                # logic to break from loop to not run infinitely
                # in case arrived at all available listings
                if scraped_listings_count == previously_counted:
                    break

    async def __do_search(self, page: Page):
        try:
            await asyncio.sleep(random() * 5)
            search_box_input_xpath = "//input[@id='searchboxinput']"
            search_box_button_xpath = "//button[@id='searchbox-searchbutton']"

            page_search_box_input = await page.wait_for_selector(
                search_box_input_xpath, timeout=10000
            )
            page_search_box_button = await page.wait_for_selector(
                search_box_button_xpath, timeout=10000
            )

            await page_search_box_input.type(self.search_query)
            await page_search_box_button.press("Enter")

            await page.wait_for_load_state("networkidle")
        except BaseException as e:
            # self.logger.error()
            print(f"error in doing search in do_search function {e}")

import asyncio
from random import random, randint
from playwright.async_api import Page
from lxml import etree


class CompleteSearchBo:
    def __init__(self, search_query):
        self.search_query = search_query

    async def complete_search(self, pages: list[Page]):
        await asyncio.gather(*[self.__do_search(page) for page in pages])
        await asyncio.gather(*[self.__scroll(page) for page in pages])

    async def __scroll(self, page: Page, total=1000):
        await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        # this variable is used to detect if the bot
        # scraped the same number of listings in the previous iteration

        previously_counted = 0
        while True:
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(randint(4000, 6500))
            scraped_listings_count = await page.locator(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            ).count()

            print(
                f"scrooling ... in page {page}, total listing = {scraped_listings_count}"
            )

            break

            if scraped_listings_count >= total:
                break

            if scraped_listings_count == previously_counted:
                break

            previously_counted = scraped_listings_count

        print("scrooling finished ...")

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

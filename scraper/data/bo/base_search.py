import traceback
import asyncio
from random import random, randint
from data.dao import BrowserPage


class BaseSearchBo:
    async def _do_search(self, browser_page: BrowserPage, search_query, recursion=0):
        if recursion >= 2:
            return
        try:
            await asyncio.sleep(randint(1, 30))
            search_box_input_xpath = "//input[@id='searchboxinput']"
            search_box_button_xpath = "//button[@id='searchbox-searchbutton']"

            page_search_box_input = await browser_page.page.wait_for_selector(
                search_box_input_xpath, timeout=120000
            )
            page_search_box_button = await browser_page.page.wait_for_selector(
                search_box_button_xpath, timeout=120000
            )

            await page_search_box_input.type(search_query)
            await page_search_box_button.press("Enter")

            await browser_page.page.wait_for_load_state("networkidle", timeout=120000)
        except BaseException as e:
            # self.logger.error()
            print(
                f"error in CompleteSearchBo in _do_search function\npage={browser_page.name}"
            )
            print(f"SCRAPER ->Error: {e}")
            traceback.print_exc()
            self._do_search(browser_page, search_query, recursion + 1)

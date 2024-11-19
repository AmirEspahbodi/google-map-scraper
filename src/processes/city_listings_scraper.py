import asyncio
from config import RuntimeResource
# import logger


class CityListingsScraperProcess:
    def __init__(self, city, place_title):
        self.resource = RuntimeResource()
        self.search_query = f"{city} in {place_title}, Iran"
        self.start_url = (
            f"https://www.google.com/maps"
        )


    async def start(self):
        chrome_page, firefox_page, safari_page = await self.open_tab()

        await asyncio.gather(
            self.goto_google_map(chrome_page),
            self.goto_google_map(firefox_page),
            self.goto_google_map(safari_page)
        )

        await asyncio.gather(
            self.complete_before_you_continue_page(chrome_page),
            self.complete_before_you_continue_page(firefox_page),
            self.complete_before_you_continue_page(safari_page)
        )
        
        await asyncio.gather(
            self.do_search(chrome_page),
            self.do_search(firefox_page),
            self.do_search(safari_page)
        )


    async def do_search(self, page):
        try:
            search_box_input_xpath = "//input[@id='searchboxinput']"
            search_box_button_xpath = "//button[@id='searchbox-searchbutton']"

            page_search_box_input = await page.wait_for_selector(search_box_input_xpath, timeout=10000)
            page_search_box_button = await page.wait_for_selector(search_box_button_xpath, timeout=10000)

            await page_search_box_input.type(self.search_query)
            await page_search_box_button.press("Enter")

            await page.wait_for_load_state("networkidle")
        except BaseException as e:
            # self.logger.error()
            print(f"error in doing search in do_search function {e}")
        finally:
            await page.close()


    async def complete_before_you_continue_page(self, page):
        pass


    async def goto_google_map(self, page):
        """
        open google map on new tab
        :param page:
        :return:
        """
        await page.goto(self.start_url, timeout=60000)
        await page.wait_for_timeout(5000)


    async def open_tab(self):
        """
        open browser abd go to google map
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

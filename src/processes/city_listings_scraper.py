import asyncio
from config import RuntimeResource


class CityListingsScraperProcess:
    def __init__(self, city, place_title):
        self.resource = RuntimeResource()
        self.start_url = f"https://www.google.com/maps/search/{city} in {place_title}, Iran"

    async def start(self):
        chrome_page, firefox_page, safari_page = await self.start_browsers_and_search()
        
        await asyncio.gather(
            self.complate_before_you_continue_page(chrome_page),
            self.complate_before_you_continue_page(firefox_page),
            self.complate_before_you_continue_page(safari_page)
        )
        
        
    async def start_browsers_and_search(self):
        chrome_page = await (await self.resource.browsers['chrome'].new_context()).new_page()
        firefox_page = await (await self.resource.browsers['firefox'].new_context()).new_page()
        safari_page = await (await self.resource.browsers['safari'].new_context()).new_page()

        await asyncio.gather(
            chrome_page.goto("https://www.google.com/maps", timeout=60000),
            firefox_page.goto("https://www.google.com/maps", timeout=60000),
            safari_page.goto("https://www.google.com/maps", timeout=60000)
        )
        await asyncio.gather(
            chrome_page.wait_for_timeout(5000),
            firefox_page.wait_for_timeout(5000),
            safari_page.wait_for_timeout(5000)
        )
        return (chrome_page, firefox_page, safari_page)

    async def complate_before_you_continue_page(self, page):
        pass
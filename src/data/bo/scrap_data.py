import asyncio
from playwright.async_api import Page

class ScrapDataBo:
    def __init__(self):
        pass

    async def scrap_page(self, *pages):
        await asyncio.gather(
            *[self.__extract_listings(page) for page in pages]
        )

        await asyncio.gather(
            *[self.__scrap_listings(page) for page in pages]
        )


    async def __scrap_listings(self, page: Page):
        pass

    async def __extract_listings(self, page: Page):
        pass
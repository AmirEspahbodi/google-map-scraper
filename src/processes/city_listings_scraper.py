from data.bo import ScrapDataBo, CompleteSearchBo, BrowserTabBo
from config import RuntimeResource
import pandas as pd
import asyncio
from playwright.async_api._generated import Page


class CityListingsScraperProcess:
    def __init__(self, city, place_title, verb):
        self.resource = RuntimeResource()
        self.search_query = f"{place_title} {verb} {city}"  # persian
        self.start_url = f"https://www.google.com/maps"
        self.browser_tab_bo = BrowserTabBo(self.start_url, self.search_query)
        self.scrap_data_bo = ScrapDataBo()
        self.complete_search_bo = CompleteSearchBo(self.search_query)

    def save(self, final_listings:dict):
        print("writing data to csv file")
        df = pd.DataFrame(final_listings)
        df.to_excel(f'{self.search_query}.xlsx', index=False)

    async def start(self):
        await self.browser_tab_bo.goto_google_map()
        await self.complete_search_bo.complete_search()
        final_listings = await self.scrap_data_bo.scrap_page()
        self.save(final_listings)
        # await self.browser_tab_bo.clear_search_bar()
        # await asyncio.gather(*[page.page.pause() for page in self.resource.browsers_pages])

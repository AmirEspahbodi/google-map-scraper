from data.bo import ScrapDataBo, CompleteSearchBo, BrowserTabBo
from config import RuntimeResource
import asyncio
from utils import save_to_excel


class CityListingsScraperProcess:
    def __init__(self):
        self.resource = RuntimeResource()
        self.start_url = f"https://www.google.com/maps"
        self.browser_tab_bo = BrowserTabBo(self.start_url)
        self.scrap_data_bo = ScrapDataBo()
        self.complete_search_bo = CompleteSearchBo()

    async def start(self):
        city = "تهران"
        verb = "در"
        place_title = "مارکت"
        await self.resource.search_query_queue.put(f"{place_title} {verb} {city}")
        while True:
            await asyncio.sleep(10) 
            if self.resource.search_query_queue.empty():
                await asyncio.sleep(10)
                continue
            
            search_query = await self.resource.search_query_queue.get()
            
            await self.resource.open_browser_tabs()
            await self.browser_tab_bo.goto_google_map()
            await self.complete_search_bo.complete_search(search_query)
            final_listings = await self.scrap_data_bo.scrap_page()
            save_to_excel(final_listings, search_query)
            await self.resource.close_browser_tabs()

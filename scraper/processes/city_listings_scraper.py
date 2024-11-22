from random import randint
from data.bo import ScrapDataBo, CompleteSearchBo, BrowserTabBo
from data.dao import RedisDao
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
        self.redis_dao = RedisDao()

    async def start(self):
        while True:
            search_query = self._redis_get_search_query()

            if not search_query:
                self.redis_dao.set_inprocessing("")
                print("queue is empty")
                await asyncio.sleep(20)
                continue

            print(search_query)

            await self.resource.open_browser_tabs()
            await self.browser_tab_bo.goto_google_map()
            await self.complete_search_bo.complete_search(search_query)
            final_listings = await self.scrap_data_bo.scrap_page()
            save_to_excel(final_listings, search_query)
            await self.resource.close_browser_tabs()
            
            await asyncio.sleep(randint(10, 15))

    def _redis_get_search_query(self):
        return self.redis_dao.dequeue()

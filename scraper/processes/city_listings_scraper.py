import gc
import asyncio
import traceback
from random import randint
from data.bo import ScrapDataBo, CompleteSearchBo, BrowserTabBo
from data.dao import RedisDao
from config import RuntimeResource, AppConfig
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
            try:
                queue_data = self._redis_get_search_query()

                if queue_data is None:
                    self.redis_dao.remove_inprocessing()
                    print("SCRAPER ->queue is empty")
                    await asyncio.sleep(20)
                    continue

                listing_category, search_query, province = queue_data

                await self.resource.initialize_browsers()
                await self.resource.open_browser_tabs()

                await self.browser_tab_bo.goto_google_map()
                await self.complete_search_bo.complete_search(
                    search_query + AppConfig.LISTING_TYPE_ITEMS_SEPARATOR + province
                )
                final_listings = await self.scrap_data_bo.scrap_page()
                if final_listings:
                    save_to_excel(
                        final_listings, listing_category, search_query, province
                    )

            except Exception as e:
                self.redis_dao.remove_inprocessing()
                print(f"SCRAPER ->Error: {e}")
                traceback.print_exc()
                await asyncio.sleep(2.5)

            finally:
                await self.resource.close_browser_tabs()
                await self.resource.free()
                gc.collect()

    def _redis_get_search_query(self):
        re = self.redis_dao.dequeue()
        if not re:
            return re
        self.redis_dao.set_inprocessing(re)
        return [d.strip() for d in re.split(AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR)]

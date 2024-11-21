from data.bo import ScrapDataBo, CompleteSearchBo, GotoMapBo


class CityListingsScraperProcess:
    def __init__(self, city, place_title, verb):
        self.search_query = f"{place_title} {verb} {city}"  # persian
        self.start_url = f"https://www.google.com/maps"
        self.scrap_data_bo = ScrapDataBo()
        self.complete_search_bo = CompleteSearchBo(self.search_query)
        self.goto_map_bo = GotoMapBo(self.start_url)

    async def start(self):
        pages = await self.goto_map_bo.goto_google_map()

        await self.complete_search_bo.complete_search(pages)

        await self.scrap_data_bo.scrap_page(pages)

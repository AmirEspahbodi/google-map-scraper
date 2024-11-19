from data.bo import ScrapDataBo, CompleteSearchBo, GotoMapBo


class CityListingsScraperProcess:
    def __init__(self, city, place_title):
        self.search_query = f"{city} in {place_title}, Iran"
        self.start_url = f"https://www.google.com/maps"
        self.scrap_data_bo = ScrapDataBo()
        self.complete_search_bo = CompleteSearchBo(self.search_query)
        self.goto_map_bo = GotoMapBo(self.start_url)

    async def start(self):
        (
            chrome_page,
            firefox_page,
            safari_page,
        ) = await self.goto_map_bo.goto_google_map()

        await self.complete_search_bo.complete_search(
            chrome_page, firefox_page, safari_page
        )

        await self.scrap_data_bo.scrap_page(chrome_page, firefox_page, safari_page)

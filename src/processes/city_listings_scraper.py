from data.bo import ScrapDataBo, CompleteSearchBo, BrowserTabBo
from config import RuntimeResource
import json
import csv



class CityListingsScraperProcess:
    def __init__(self, city, place_title, verb):
        self.resource = RuntimeResource()
        self.search_query = f"{place_title} {verb} {city}"  # persian
        self.start_url = f"https://www.google.com/maps"
        self.browser_tab_bo = BrowserTabBo(self.start_url)
        self.scrap_data_bo = ScrapDataBo()
        self.complete_search_bo = CompleteSearchBo(self.search_query)

    def save(self, final_listings:dict):
        with open(self.search_query, 'w') as fpw:
            csv_writer = csv.writer(fpw)
            count = 0
            for listing in final_listings:
                if count == 0:
                    # Writing headers of CSV file
                    header = listing.keys()
                    csv_writer.writerow(header)
                    count += 1
                # Writing data of CSV file
                csv_writer.writerow(listing.values())

    async def start(self):
        await self.browser_tab_bo.clear_search_bar()
        await self.browser_tab_bo.goto_google_map()
        await self.complete_search_bo.complete_search()
        final_listings = await self.scrap_data_bo.scrap_page()
        for re in final_listings:
            print(re)

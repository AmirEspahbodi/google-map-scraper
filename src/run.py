import asyncio
from processes import CityListingsScraperProcess
from config import RuntimeResource


async def main():
    resource = RuntimeResource()
    await resource.initialize_browsers()
    await resource.open_browser_tabs()

    city_listings_scraper = CityListingsScraperProcess(city, place_title, verb)
    await city_listings_scraper.start()

    await resource.free()


if __name__ == "__main__":
    # city = input("enter city name: ")
    # title = input("enter place base title: ")
    city = "تهران"
    verb = "در"
    place_title = "مارکت"
    asyncio.run(main())

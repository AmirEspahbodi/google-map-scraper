import asyncio
from processes import CityListingsScraperProcess
from config import RuntimeResource


async def main():
    resource = RuntimeResource()
    await resource.initialize_browsers()

    city_listings_scraper = CityListingsScraperProcess(city, place_title)
    await city_listings_scraper.start()

    await resource.free()


if __name__ == "__main__":
    # city = input("enter city name: ")
    # title = input("enter place base title: ")
    city = "sari"
    place_title = "store"
    asyncio.run(main())

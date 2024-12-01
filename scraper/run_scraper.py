import asyncio
from processes import CityListingsScraperProcess
from config import RuntimeResource


async def main():
    resource = RuntimeResource()

    city_listings_scraper = CityListingsScraperProcess()
    await city_listings_scraper.start()



if __name__ == "__main__":
    # city = input("enter city name: ")
    # title = input("enter place base title: ")
    asyncio.run(main())

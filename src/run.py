import asyncio
from processes import CityPlaceScraper
from config import RuntimeResource


async def main():
    await resource.initialize_browsers()

    city_place_scraper = CityPlaceScraper(city, place_title)
    await city_place_scraper.start()

    await resource.free()


if __name__ == "__main__":
    # city = input("enter city name: ")
    # title = input("enter place base title: ")
    city = "ساری"
    place_title = "سوپر مارکت"
    resource = RuntimeResource()
    asyncio.run(main())

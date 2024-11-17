import asyncio
from processes.gmap import GMap
from config import RuntimeResource


async def main():
    await resource.initialize_browsers()

    gmap = GMap(city, place_title)
    await gmap.start()

    await resource.free()


if __name__ == "__main__":
    # city = input("enter city name: ")
    # title = input("enter place base title: ")
    city = "ساری"
    place_title = "سوپر مارکت"
    resource = RuntimeResource()
    asyncio.run(main())

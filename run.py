import asyncio
from src.processes.gmap import GMap

async def main():
    gmap = GMap()
    await gmap.start()


if __name__ == "__main__":
    city = input("enter city name: ")
    title = input("enter place base title: ")
    asyncio.run(main())

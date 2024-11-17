from config import RuntimeResource


class GMap:
    def __init__(self, city, place_title):
        self.resource = RuntimeResource()
        self.start_url = f"https://www.google.com/maps/search/{city}+{place_title}"

    async def request(self, city, place_title):
        pass

    async def start(self):
        pass

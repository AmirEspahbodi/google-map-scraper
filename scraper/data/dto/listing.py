from pydantic import BaseModel, ConfigDict


class Listing(BaseModel):
    title: str | None
    description: str | None
    phone_numbers: list[str] | None
    address: str | None
    map_location: str | None
    map_city: str | None
    map_state: str | None
    website: str | None
    reviews_count: int | None
    reviews_average: float | None
    latitude: float | None
    longitude: float | None

    model_config = ConfigDict()


class ListingsList:
    listings: Listing

    def __init__(self, listings):
        self.listings = listings

    def save_to_csv(self):
        pass

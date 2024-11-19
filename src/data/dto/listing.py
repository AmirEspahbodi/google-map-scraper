from pydantic import BaseModel, ConfigDict


class Listing(BaseModel):
    title: str | None
    description: str | None
    phone_numbers: list[str] | None
    address: str | None
    map_location: str | None
    map_city: str | None
    map_state: str | None
    model_config = ConfigDict()

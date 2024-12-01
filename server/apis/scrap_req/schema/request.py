from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    province: str
    city: str
    verb: str
    listing_type: str
    listing_category: str
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "province": "تهران",
                    "city": "تهران",
                    "verb": "در",
                    "listing_type": "آبمیوه و بستنی",
                    "listing_category": "فروشگاه و کسب و کار های محلی",
                },
                {
                    "province": "تهران",
                    "city": "کرج",
                    "verb": "در",
                    "listing_type": "دیزی سرا",
                    "listing_category": "خدمات غذایی و پذیرایی",
                },
            ]
        },
    )

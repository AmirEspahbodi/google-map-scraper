from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    city: str = Field(..., example="تهران")
    verb: str = Field(..., example="در")
    place_title: str = Field(..., example="مارکت")

    model_config = ConfigDict(
        json_schema_extra={
            "city": "تهران",
            "verb": "در",
            "place_title": "مارکت"
        },
    )

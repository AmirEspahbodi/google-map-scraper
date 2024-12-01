from pydantic import BaseModel, Field


class ResponseBody(BaseModel):
    imported_requests: list[str] | None = Field(default_factory=[])
    not_imported_requests: list[str] | None = Field(default_factory=[])
    in_process: str | None = Field(default_factory="")
    waiting_to_scrape: list[str] | None = Field(default_factory=[])

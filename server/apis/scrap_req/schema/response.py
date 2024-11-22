from pydantic import BaseModel, Field


class ResponseBody(BaseModel):
    completed: list[str] | None = Field(default_factory=[])
    in_process: str | None = Field(default_factory=[])
    waiting: list[str] | None = Field(default_factory=[])

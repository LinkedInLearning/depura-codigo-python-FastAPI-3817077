from typing import Optional

from pydantic import BaseModel, Field


class ReviewSchema(BaseModel):
    opinion: str = Field(max_length=500)
    rate: int = Field(ge=1, le=5)

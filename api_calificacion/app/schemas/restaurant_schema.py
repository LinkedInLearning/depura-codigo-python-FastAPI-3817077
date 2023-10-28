from pydantic import BaseModel, Field


class RestaurantSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    address: str = Field(max_length=100)

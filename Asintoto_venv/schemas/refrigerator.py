from pydantic import BaseModel, ConfigDict
from typing import List
from .food import Food

class Refrigerator(BaseModel):
    id: int
    name: str
    location: str
    foods: List[Food] = []

    model_config = ConfigDict(from_attributes=True)

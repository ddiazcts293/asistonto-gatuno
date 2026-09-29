from pydantic import BaseModel, ConfigDict
from datetime import date

class Food(BaseModel):
    id: int
    name: str
    type: str
    quantity: int
    best_before: date

    model_config = ConfigDict(from_attributes=True)

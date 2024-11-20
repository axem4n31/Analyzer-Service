from pydantic import BaseModel
from typing import List
from datetime import date


class ProductSchema(BaseModel):
    id: int
    name: str
    quantity: int
    price: float
    category: str


class SalesDataSchema(BaseModel):
    date: date
    products: List[ProductSchema]

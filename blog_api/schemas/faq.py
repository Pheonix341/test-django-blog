from ninja import Schema
from typing import Optional

class FAQSchema(Schema):
    id: int
    title: str
    description: str

class FAQCreateSchema(Schema):
    title: str
    description: str

class FAQUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None


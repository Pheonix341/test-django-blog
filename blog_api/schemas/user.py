from ninja import Schema
from typing import Optional

class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    
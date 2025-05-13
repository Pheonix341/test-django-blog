import typing
from ninja import Schema
from datetime import datetime


class UserLoginSchema(Schema):
    username: str
    password: str
    
class UserRegistrationSchema(Schema):
    username: str
    email: str
    first_name: str   
    password1: str
    password2: str
    
class UserOutSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str   
    date_joined: datetime
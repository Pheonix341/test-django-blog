from ninja import Schema


class SliderSchema(Schema):
    id: int
    title: str
    description: str
    image: str
    
class SliderCreateSchema(Schema):
    title: str
    description: str
    
class SliderDetailSchema(Schema):
    image: list["SliderImageSchema"]


class SliderImageSchema(Schema):
    id: int
    image: str
    

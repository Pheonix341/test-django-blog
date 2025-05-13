import typing
from ninja import Schema
from datetime import datetime
from .category import CategorySchema

class ArticleAuthorSchema(Schema):
    id: int
    username: str

class ArticleListSchema(Schema):
    id: int
    name: str
    short_description: str
    preview: typing.Optional[str]
    views: int
    category: CategorySchema
    author: ArticleAuthorSchema
    created_at: datetime
    
class ArticleDetailSchema(Schema):
    id: int
    name: str
    full_description: typing.Optional[str]
    views: int
    category: CategorySchema
    author: ArticleAuthorSchema
    images: list["ArticleImageSchema"]
    comment: list["ArticleCommentSchema"]
    
    total_likes: int = 0
    total_dislikes: int = 0
    total_comments: int = 0
    
    created_at: datetime
    updated_at: datetime
    
    @staticmethod
    def resolve_total_likes(obj):
        return obj.likes.user.all().count()   
             
    @staticmethod    
    def resolve_total_dislikes(obj):
        return obj.dislikes.user.all().count()
        
    @staticmethod    
    def resolve_total_comments(obj):
        return obj.comments.all().count()
                
    
class ArticleImageSchema(Schema):
    id: int
    image: str
    
class ArticleCommentSchema(Schema):
    id: int
    author: ArticleAuthorSchema
    text: str
    created_at: datetime
    
class ArticleCreateSchema(Schema):
    name: str
    short_description: str
    full_description: typing.Optional[str]
    category: int
    author: int
    
    
class ArticleUpdateSchema(Schema):
    name: typing.Optional[str] = None
    short_description: typing.Optional[str] = None
    full_description: typing.Optional[str] = None
    category: typing.Optional[str] = None
    
class ArticleVoteSchema(Schema):
    user_id: int
    action: str
    
    
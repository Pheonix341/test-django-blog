import typing
import os
from ninja import Router, File
from ninja.files import UploadedFile
from ninja.security import django_auth

from blog_app.models import Article, Category, ArticleImage
from django.contrib.auth.models import User


from blog_api.schemas.article import (
    ArticleListSchema,
    ArticleDetailSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema,
    ArticleVoteSchema
)
from django.shortcuts import get_object_or_404
from blog.settings import BASE_DIR
from blog_api.services.articles import article_service


router = Router(tags=['Articles'])

@router.get('/articles/', response=list[ArticleListSchema])
def get_all_articles(request):
    return article_service.get_all_articles(request)

@router.post('/articles/', response=ArticleDetailSchema)
def create_new_article(request, data: ArticleCreateSchema, preview: UploadedFile = File(...), gallery: list[UploadedFile] = File(...)):
    return article_service.create_new_article(data, preview, gallery)
    

@router.get('/articles/{article_id}/', response=ArticleDetailSchema)
def get_article_detail(request, article_id: int):
    return article_service.get_article_detail(article_id)

@router.patch('/articles/{article_id}/update/', response=ArticleDetailSchema)
def update_article(request, 
    article_id: int, 
    data: ArticleUpdateSchema, 
    preview: typing.Optional[UploadedFile] = File(None),
    gallery: typing.Optional[list[UploadedFile]] = File(None)
):
    return article_service.update_article(article_id, data, preview, gallery)       
                    
            
            
    

@router.delete('/articles/{article_id}/')
def delete_article(request, article_id: int):
    return article_service.delete_article(article_id)
    
    
@router.post('/articles/{article_id}/add_vote')
def add_like_or_dislike(request, article_id: int, vote_data: ArticleVoteSchema):
    return article_service.add_vote(article_id=article_id, vote_data=vote_data)
    
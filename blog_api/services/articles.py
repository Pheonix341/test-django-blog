from django.http import HttpRequest
from blog_app.models import Article, ArticleImage, Category, Like, Dislike
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from ninja import UploadedFile, File
from blog_api.schemas.article import ArticleCreateSchema, ArticleUpdateSchema, ArticleVoteSchema
from typing import Optional
from blog.settings import BASE_DIR
import os
from ninja.errors import ValidationError



class ArticleService:
    def get_all_articles(self, request: HttpRequest) -> list[Article]:
        """returns all Article objects from db."""
        article = Article.objects.all()
        return article
        
    def get_article_detail(self, article_id: int) -> Article:
        article = get_object_or_404(Article, pk=article_id)
        return article
        
        
    def create_new_article(self, data: ArticleCreateSchema, 
        preview: Optional[UploadedFile] = File(None), 
        gallery: Optional[list[UploadedFile]] = File(None)
    ):
        _data = data.dict()
    
        category = get_object_or_404(Category, pk=_data.pop('category'))
        author = get_object_or_404(User, pk=_data.pop('author'))
        
        preview_bytes = preview.read()
        with open(f'{BASE_DIR}/media/images/articles/previews/{preview.name}',mode='wb') as file:
            file.write(preview_bytes)        
            
        article = Article.objects.create(**_data, category=category, author=author)
        article.preview = f'images/articles/previews/{preview.name}'
        article.save()
        
        for item in gallery:
            item_bytes = item.read()
            with open(f'{BASE_DIR}/media/articles/gallery/{item.name}',mode='wb') as file:
                file.write(item_bytes)
                
            obj = ArticleImage.objects.create(
                article=article,
                image=f'articles/gallery/{item.name}'
            )
        
        return article
    
    def update_article(self, 
        article_id: int, 
        data: ArticleUpdateSchema, 
        preview: Optional[UploadedFile] = File(None),
        gallery: Optional[list[UploadedFile]] = File(None)
    ):    
        article = get_object_or_404(Article, pk=article_id)
        items = data.dict()
        for key, value in items.items():
            if value is None:
                current_value=getattr(article, key)
                setattr(article, key, current_value)
            else:
                if key == 'category':
                    category = get_object_or_404(Category, pk=value)
                    setattr(article, key, category)
                else:
                    setattr(article, key, value)
                    
        if preview is not None:
            preview_content = preview.read()
            previews_folder_path = f'{BASE_DIR}/media/images/articles/previews'
            previews_files = os.listdir(previews_folder_path)
            if preview.name not in previews_files:
                print('NO PREVIEW FILE IN LIST')
                with open(f'{previews_folder_path}/{preview.name}', mode='wb') as _file:
                        _file.write(preview_content)
                if not article.preview:
                    article.preview = f'images/articles/previews/{preview.name}'
                else:
                    os.remove(f'{previews_folder_path}/{preview.name}')
                    article.preview = f'images/articles/previews/{preview.name}'
            else:
                article.preview = f'images/articles/previews/{preview.name}'
                
        if gallery is not None:
            for item in article.images.all():
                os.remove(f'{BASE_DIR}/{item.image.url}')
                item.delete()
            
            for item in gallery:
                item_bytes = item.read()
            with open(f'{BASE_DIR}/media/articles/gallery/{item.name}',mode='wb') as file:
                file.write(item_bytes)
                
            obj = ArticleImage.objects.create(
                article=article,
                image=f'articles/gallery/{item.name}'
            )
            article.save()                
        return article
        
    def delete_article(self, article_id: int):
        article = get_object_or_404(Article, pk=article_id)
        article.delete()
        return {'is_deleted': True}
        
    def add_vote(self, article_id: int, vote_data: ArticleVoteSchema):
        article = get_object_or_404(Article, pk=article_id)
        user = get_object_or_404(User, pk=vote_data.user_id)
        
        if vote_data.action not in ['add_like', 'add_dislike']:
            raise ValidationError('invalid action')
            
        try:
            article.likes
        except Exception as e:
            Like.objects.create(article=article)
            
        try:
            article.dislikes
        except Exception as e:
            Dislike.objects.create(article=article)            
        
        
        if vote_data.action == 'add_like':
            if user in article.likes.user.all():
                article.likes.user.remove(user.id)
            else:
                article.likes.user.add(user.id)
                article.dislikes.user.remove(user.id)
            return {'is_liked': True, 'is_liked': False}                
        elif vote_data.action == 'add_dislike':
            if user in article.likes.user.all():
                article.dislikes.user.remove(user.id)
            else:
                article.dislikes.user.add(user.id)
                article.likes.user.remove(user.id)
            return {'is_liked': False, 'is_dislike': True}
                
    
    
        
article_service = ArticleService()
        
        
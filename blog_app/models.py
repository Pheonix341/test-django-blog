from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# название
# поля
# тип данных поля

# blog_app_slider
class Slider(models.Model):
    # verbose_name = альтернативное название для поля
    title = models.CharField(max_length=100, verbose_name='Заголовок')  # varchar
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/slider/',  verbose_name='Фотография')
    # media/images/slider/slide.png
    
    def __str__(self):
        return self.title

# python manage.py makemigrations
# python manage.py migrate

class FAQ(models.Model):
    # question = models.CharField(max_length=255)
    title = models.CharField(max_length=255, verbose_name='Вопрос')
    # answer = models.TextField()
    description = models.TextField(verbose_name='ответ')
    
    def __str__(self) -> str:
        return self.title
    

# спорт -> sport

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг', help_text='Это поле заполняется само')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    

class Article(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', null=True, blank=True)
    preview = models.ImageField(upload_to='images/articles/previews/', blank=True, null=True, verbose_name='Фото')
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
        


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
        verbose_name='Статья', related_name='images'
    )
    image = models.ImageField(upload_to='articles/gallery/', verbose_name='Фото')
    
    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural = 'Галлереи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
        verbose_name='Статья', related_name='comment'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    
class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f'{self.article} - {self.user}'
        
    class Meta:
        verbose_name = 'Просмотр статьи'
        verbose_name_plural = 'Просмотры статей'

# python manage.py makemigrations
# python manage.py migrate


class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')
    
    
class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')
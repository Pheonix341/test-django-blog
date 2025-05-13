from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, CommentForm, ArticleForm
from . import models
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.

def display_home_page(request):
    slider_objects = models.Slider.objects.all()  # select * from blog_app_slider
    faqs = models.FAQ.objects.all()
    articles = models.Article.objects.all()
    
    paginator = Paginator(articles, 2)  # [(1, [1,2]), (2, [3,4]), (3, [5,6])]
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'slider_objects': slider_objects,
        'faqs': faqs,
        'articles': articles
    }
    return render(request, 'blog_app/index.html', context)


def display_about_page(request):
    return render(request, 'blog_app/about.html')


def display_contacts_page(request):
    return render(request, 'blog_app/contacts.html')


def display_faq_page(request):
    faqs = models.FAQ.objects.all()
    context = {
        'faqs': faqs
    }
    return render(request, 'blog_app/faq.html', context)
    
def display_articles_page(request):
    query = request.GET.get('category')
    
    categories = models.Category.objects.all()
    articles = models.Article.objects.all()
    
    if query:
        category = categories.get(slug=query)
        articles = articles.filter(category=category)
    
    paginator = Paginator(articles, 2)  # [(1, [1,2]), (2, [3,4]), (3, [5,6])]
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'categories': categories,
        'articles': articles
    }
    return render(request, 'blog_app/articles_list.html', context)

# получить список объектов класса ArticleImage которые ссылаются на статью
# отдать в контексте новый ключ
# отобразить фотографии на детальной странице

def display_article_detail_page(request, pk):
    article = models.Article.objects.get(pk=pk)
    comments = models.Comment.objects.filter(article=article)
    images = models.ArticleImage.objects.filter(article=article)
    
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            messages.success(request, 'Комментарий успешно добавлен')
            return redirect('detail', pk=article.pk)
    else:
        form = CommentForm()
    
    if request.user.is_authenticated:
        is_viewed = models.ArticleView.objects.filter(
            article=article,
            user=request.user
        ).exists()  # True, False
        
        if not is_viewed:
            models.ArticleView.objects.create(
                article=article,
                user=request.user
            )
            article.views += 1
            article.save()
    
    try:
        article.likes
    except Exception as e:
        models.Like.objects.create(article=article)
    
    try:
        article.dislikes
    except Exception as e:
        models.Dislike.objects.create(article=article)
        
    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()
    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'images': images,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes
    }
    return render(request, 'blog_app/article_detail.html', context)


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            
            article = models.Article.objects.get(pk=form.pk)
            for obj in request.FILES.getlist('gallery'):
                img = models.ArticleImage.objects.create(
                    image=obj,
                    article=article
                )
                
                
            messages.success(request, 'Статья была успешно создана')
            return redirect('detail', pk=form.pk)
    else:
        form = ArticleForm()
    
    context = {
        'form': form
    }
            
    return render(request, 'blog_app/article_form.html', context)
    


""" 
сделать функцию для отображения страницы создания статьи
создать ссылку для этой страницы
создать кнопку для перехода на страницу
 """


'''
создать таблицу для фотографий статьи

таблица должна ссылаться на статью
и должно поле для фотографии

articles/gallery/

ArticleImage
article = 
image = 

class Meta:
    
'''


def display_login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            print('0 [INFO] - WORK')
            user = form.get_user()  # получаем объект пользователя по введенным данным User\None
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'Успешно вошли в аккаунт')
                return redirect('home')
            else:
                print('1 [INFO] - WORK')
                messages.error(request, 'Пользователь не найден')
    else:
        form = LoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'blog_app/login.html', context)
    
def display_registration_page(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, 'blog_app/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


class ArticleUpdate(UpdateView):
    model = models.Article
    form_class = ArticleForm
    # success_url = '/articles/'
    template_name = 'blog_app/article_form.html'
    
    def post(self, request, *args, **kwargs):
        article = self.get_object()
        images = models.ArticleImage.objects.filter(article=article)
        for image in images:
            image.delete()
        
        for obj in request.FILES.getlist('gallery'):
            print(obj)
            image = models.ArticleImage.objects.create(
                article=article,
                image=obj
            )
        
                
        
        return super().post(request, *args, **kwargs)
    

class ArticleDelete(DeleteView):
    model = models.Article
    template_name = 'blog_app/article_confirm_delete.html'
    success_url = '/articles/'
    

def add_vote(request, article_id, action):
    article = models.Article.objects.get(pk=article_id)
    
    # add_like, add_dislike
    user = request.user
    
    if action == 'add_dislike':
        if user in article.dislikes.user.all():
            article.dislikes.user.remove(user.pk)
        else:
            article.dislikes.user.add(user.pk)
            article.likes.user.remove(user.pk)
    if action == 'add_like':
        if user in article.likes.user.all():
            article.likes.user.remove(user.pk)
        else:
            article.likes.user.add(user.pk)
            article.dislikes.user.remove(user.pk)
    
    return redirect('detail', pk=article.pk)
    
    
def search(request):
    query = request.GET.get('q')
    articles = models.Article.objects.filter(name__iregex=query)
    context = {
        'articles': articles,
        'total_articles': articles.count(),
        'query': query
    }
    return render(request, 'blog_app/search.html', context)
    

@login_required(login_url='login')    
def display_profile_page(request):
    articles = models.Article.objects.filter(author=request.user)
    total_views = sum([article.views for article in articles])
    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])
    context ={
        'total_articles': articles.count(),
        'total_views': total_views,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'articles': articles
    }
    return render(request, 'blog_app/profile.html', context)
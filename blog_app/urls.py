from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_home_page, name='home'),
    path('about/', views.display_about_page, name='about'),
    path('contacts/', views.display_contacts_page, name='contacts'),
    path('faq/', views.display_faq_page, name='faq'),
    path('articles/', views.display_articles_page, name='articles'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:pk>/', views.display_article_detail_page, name='detail'),
    path('articles/<int:article_id>/<str:action>/', views.add_vote, name='add_vote'),
    path('login/', views.display_login_page, name='login'),
    path('registration/', views.display_registration_page, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('articles/<int:pk>/update/', views.ArticleUpdate.as_view(), name='update'),
    path('articles/<int:pk>/delete/', views.ArticleDelete.as_view(), name='delete'),
    path('search/', views.search, name='search'),
    path('profile/', views.display_profile_page, name='profile')
    
]
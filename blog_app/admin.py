from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}



class ArticleImageInline(admin.TabularInline):
    model = models.ArticleImage
    


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'author']
    list_display_links = ['id', 'name']
    # prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views']
    list_filter = ['category', 'author', 'created_at']
    list_editable = ['category', 'author']
    inlines = [ArticleImageInline]

admin.site.register(models.Slider)
admin.site.register(models.FAQ)
admin.site.register(models.Comment)


'''
отобрзаить комментарии для статьи на детальной странице статьи

1) получить комментарии для статьи из базы данных
2) полученный список комментариев отдать в контекст
3) в html файле написать цикл по полученному списку
4) вывести атрибуты объекта класса комментария в html

'''
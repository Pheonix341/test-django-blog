from ninja import Router
from blog_api.schemas.slider import SliderSchema, SliderDetailSchema, SliderCreateSchema
from blog_app.models import Slider
from django.shortcuts import get_object_or_404
from ninja.files import UploadedFile




router = Router(tags=['Slider'])

@router.get('/sliders/', response=list[SliderSchema])
def get_slider_items(request):
    items = Slider.objects.all()
    return items
    
# @router.post('/sliders/', response=SliderDetailSchema)
# def create_new_slider(request, data: SliderCreateSchema, preview: UploadedFile = file(...), gallery: list[UploadedFile] = file(...)):
#     print(data.dict())
#     _data = data.dict()
# preview_bytes = preview.read()
    # with open(f'{BASE_DIR}/media/images/articles/previews/{preview.name}',mode='wb') as file:
    #     file.write(preview_bytes)        
        
    # article = Article.objects.create(**_data, category=category, author=author)
    # article.preview = f'images/articles/previews/{preview.name}'
    # article.save()
    
    # for item in gallery:
    #     item_bytes = item.read()
    #     with open(f'{BASE_DIR}/media/articles/gallery/{item.name}',mode='wb') as file:
    #         file.write(item_bytes)
            
    #     obj = ArticleImage.objects.create(
    #         article=article,
    #         image=f'articles/gallery/{item.name}'
    #     )
    
    # return article



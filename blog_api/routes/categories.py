from ninja import Router
from django.shortcuts import get_object_or_404
from blog_app.models import Category
from blog_api.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from slugify import slugify


router = Router(tags=['Categories'])

@router.get('/categories/', response=list[CategorySchema])
def get_all_categories(request):
    categories = Category.objects.all()
    return categories
    
    
@router.get('/categories/{category_id}/', response=CategorySchema)
def get_category_detail(request, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    return category
    
@router.patch('/categories/{category_id}/update/')
def update_category(request, category_id: int, data: CategoryUpdateSchema):
    category = get_object_or_404(Category, pk=category_id)
    items = data.dict()
    print(items)
    for key, value in items.items():
        if value is None:
            current_value=getattr(category, key)
            setattr(category, key, current_value)
        else:
            setattr(category, key, value)
            
    category.save()
    return category
    
@router.post('/categories/', response=CategorySchema)
def create_new_category(request, data: CategoryCreateSchema):
    new_category = Category.objects.create(
        name=data.name,
        slug=slugify(data.name)
    )
    return new_category
    

from ninja import Router
from blog_api.schemas.faq import FAQSchema, FAQCreateSchema, FAQUpdateSchema
from blog_app.models import FAQ
from django.shortcuts import get_object_or_404




router = Router(tags=['FAQ'])

@router.get('/faqs/', response=list[FAQSchema])
def get_all_faq_items(request):
    items = FAQ.objects.all()
    return items
    
@router.get('/faqs/{faq_id}/', response=FAQSchema)
def get_faq_detail(request, faq_id: int):
    faq = get_object_or_404(FAQ, pk=faq_id)
    return faq
    
@router.post('/faqs/', response=FAQSchema)
def create_faq(request, data: FAQCreateSchema):
    new_faq = FAQ.objects.create(
        title=data.title,
        description=data.description
    )
    return new_faq
    
@router.patch('/faqs/{faq_id}/', response=FAQSchema)
def update_daq_item(request, faq_id: int, data: FAQUpdateSchema):
    faq = get_object_or_404(FAQ, pk=faq_id)
    items = data.dict()
    for key, value in items.items():
        if value is None:
            current_value=getattr(faq, key)
            setattr(faq, key, current_value)
        else:
            setattr(faq, key, value)
            
    faq.save()
    return faq
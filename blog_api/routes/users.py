from ninja import Router, File
from django.contrib.auth.models import User
from blog_api.schemas.user import UserSchema

router = Router(tags=['Users'])

@router.get('/users/', response=list[UserSchema])
def get_users(request):
    users = User.objects.all()
    return users
    
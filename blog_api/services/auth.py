from django.http import HttpRequest
from blog_api.schemas.auth import UserLoginSchema, UserRegistrationSchema
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from ninja.errors import ValidationError




class AuthService:
    def user_login(self, request: HttpRequest, user_login_data:UserLoginSchema):
        user = authenticate(
        username=user_login_data.username,
        password=user_login_data.password
    )
        if user is None:
            raise ValidationError(errors='User not found')
            
        login(request, user)
        return {'is_authenticated': user.is_authenticated}
        
    
    def registor_user(self, user_register_data:UserRegistrationSchema):
        if User.objects.filter(username=user_register_data.username).exists():
            raise ValidationError(errors='Пользователь с таким username уже есть')
                
        data = user_register_data.dict()
        password1 = data.pop('password1')
        password2 = data.pop('password2')
        
        if password1 != password2:
            raise ValidationError(errors='Пароли не совпадают')
            
        email = user_register_data.email
        if '.' not in email or '@' not in email:
            raise ValidationError(errors='Неверный формат почты')
            
        user = User.objects.create(**data)
        user.set_password(password1)
        user.save()
        return user
    
    def user_logout(self, request:HttpRequest):
        logout(request)
        user = request.user    
        return {'is_authenticated': user.is_authenticated}
        
auth_service = AuthService()
    
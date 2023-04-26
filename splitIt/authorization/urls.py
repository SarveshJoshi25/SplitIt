from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from splitIt.authorization.views import CreateAccount, UserLogin, AuthenticateUser, RefreshToken

urlpatterns = [
    path('join/', CreateAccount.as_view(), name='CreateAccount'),
    path('login/', UserLogin.as_view(), name='UserLogin'),
    path('authenticate/', AuthenticateUser.as_view(), name='AuthenticateUser'),
    path('refresh/', RefreshToken.as_view(), name='RefreshToken'),

]

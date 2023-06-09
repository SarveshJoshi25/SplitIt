from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from splitIt.authorization.views import CreateAccount, UserLogin, RefreshToken, LogoutUser, \
    VerifyEmailAddress, ResendVerificationEmail

urlpatterns = [
    path('signup/', CreateAccount.as_view(), name='CreateAccount'),
    path('login/', UserLogin.as_view(), name='UserLogin'),
    path('refresh/', RefreshToken.as_view(), name='RefreshToken'),
    path('logout/', LogoutUser.as_view(), name='LogoutUser'),
    path('verify/<str:verify>/', VerifyEmailAddress.as_view(), name='VerifyEmailAddress'),
    path('resend/verification/', ResendVerificationEmail.as_view(), name='ResendVerificationEmail'),
]

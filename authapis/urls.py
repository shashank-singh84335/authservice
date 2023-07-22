from django.urls import path
from authapis.views import *

urlpatterns = [
    path("signup", SignUpView.as_view(), name='signup'),
    path("signin", SignInView.as_view(), name='signin'),
    path("signout", SignOutView.as_view(), name='signout'),
    path("forgot_password", ForgotPasswordView.as_view(), name='forgot_password'),
    path("refresh_token", RefreshTokenView.as_view(), name='refresh_token'),

]
from django.urls import path
from .views import user_login, user_logout, user_register, email_verification_sent


urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", user_register, name="register"),
    path("email-verification-sent/", email_verification_sent, name="email_verification_sent"),
]

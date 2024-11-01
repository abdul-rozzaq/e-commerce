from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    user_login,
    user_logout,
    user_register,
    email_verification_sent,
    resend_verification,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)


urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", user_register, name="register"),
    path("email-verification-sent/", email_verification_sent, name="email_verification_sent"),
    path("resend-verification-email/", resend_verification, name="resend_verification"),
    # Reset Password
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password-reset/password_reset.html",
            html_email_template_name="emails/password_reset_msg.html",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password-reset/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password-reset/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password-reset/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

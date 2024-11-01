from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView

from verify_email.email_handler import send_verification_email, resend_verification_email

from .forms import UserRegisterForm, UserLoginForm
from .models import User


def user_register(request: WSGIRequest):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            send_verification_email(request, form)

            return redirect("email_verification_sent")
    else:
        form = UserRegisterForm()

    context = {"form": form}

    return render(request, "accounts/register.html", context)


def user_login(request: WSGIRequest):
    context = {"errors": []}
    next = request.GET.get("next")

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.get_user(email, password)

            if user:
                if user.is_active:
                    login(request=request, user=user)

                    return redirect(next or "home_page")

                request.session["temp_email"] = user.email

                return redirect("resend_verification")

            else:
                context["errors"] = ["User topilmadi. Email yoki parol xato."]

    else:
        form = UserLoginForm()

    context["form"] = form

    return render(request, "accounts/login.html", context)


def user_logout(request: WSGIRequest):

    logout(request)

    return redirect("login")


def email_verification_sent(request):
    return render(request, "verifications/email_verification_sent.html")


def resend_verification(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user and not user.is_active:
            resend_verification_email(request, email, user=user, encoded=False)

            messages.success(request, "Tasdiqlash emaili qayta yuborildi.")
            return redirect("email_verification_sent")
        else:
            messages.error(request, "Email manzil topilmadi yoki foydalanuvchi allaqachon tasdiqlangan.")

    return render(request, "accounts/resend_email_verification.html")


def password_reset(request):
    context = {}
    return render(request, "accounts/password-reset/password_reset.html", context)


def password_reset_done(request):
    context = {}
    return render(request, "accounts/password-reset/password_reset_done.html", context)


def password_reset_confirm(request):
    context = {}
    return render(request, "accounts/password-reset/password_reset_confirm.html", context)


def password_reset_complete(request):
    context = {}
    return render(request, "accounts/password-reset/password_reset_complete.html", context)

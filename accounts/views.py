from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.handlers.wsgi import WSGIRequest
from verify_email.email_handler import send_verification_email

from .forms import UserRegisterForm, UserLoginForm


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
            login(request=request, user=form.get_user())

            return redirect(next or "home_page")

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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required


# @login_required(login_url="login")
def home_page(request):
    return render(request, "index.html", {})


def cart_page(request):
    context = {}
    return render(request, "cart.html", context)


def checkout_page(request):
    context = {}
    return render(request, "checkout.html", context)


def contact_page(request):
    context = {}
    return render(request, "contact.html", context)


def detail_page(request):
    context = {}
    return render(request, "detail.html", context)


def shop_page(request):
    context = {}
    return render(request, "shop.html", context)


def test(request):
    return render(request, "verifications/email_verification_successful.html")

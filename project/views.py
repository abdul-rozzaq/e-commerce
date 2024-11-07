from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from project.forms import CartItemForm, ReviewForm

from .models import (CartItem, Category, Product, ProductColor, ProductSize,
                     Review)


class HomePageView(generic.ListView):
    model = Category
    context_object_name = "categories"
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()

        context["products"] = Product.objects.all().order_by("?")[:8]
        context["carousel_items"] = categories.order_by("?")[:3]

        return context


class SearchProductsView(generic.ListView):
    template_name = "shop.html"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get("query", "")
        category = self.request.GET.get("category", None)
        colors = self.request.GET.getlist("colors", [])
        sizes = self.request.GET.getlist("sizes", [])

        if category:
            queryset = queryset.filter(category_id=category)

        if colors:
            queryset = queryset.filter(colors__in=colors).distinct()

        if sizes:
            queryset = queryset.filter(sizes__in=sizes).distinct()

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query)).distinct()

        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", 12)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["colors"] = ProductColor.objects.all()
        context["sizes"] = ProductSize.objects.all()

        context["selected_colors"] = [int(n) for n in self.request.GET.getlist("colors")]
        context["selected_sizes"] = [int(n) for n in self.request.GET.getlist("sizes")]

        return context


class DetailPage(generic.DetailView):
    template_name = "detail.html"
    model = Product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["random_products"] = Product.objects.all().order_by("?")[:8]

        return context

    def post(self, request: WSGIRequest, *args, **kwargs):
        form = ReviewForm(request.POST)
        user = request.user

        if form.is_valid():
            review: Review = form.save(commit=False)

            review.product = self.get_object()
            review.user = user if request.user.is_authenticated else None

            review.save()

        return super().get(request, *args, **kwargs)


class CheckOutView(LoginRequiredMixin, generic.View):
    def post(self, request: WSGIRequest, product_id, *args, **kwargs):

        form = CartItemForm(request.POST)

        if form.is_valid():
            cart_item: CartItem = form.save(commit=False)

            cart_item.product_id = product_id
            cart_item.user = request.user

            cart_item.save()

            return redirect("cart_page")

        print(form.errors)

        return redirect("detail_page", pk=product_id)

    def get_redirect_field_name(self) -> str:
        return "home_page"


class ShoppingCartView(LoginRequiredMixin, generic.TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        items = CartItem.objects.filter(user=self.request.user)
        shipping = 10

        context["cart_items"] = items
        context["shipping"] = shipping
        context["total_price"] = float(items.aggregate(total=Sum(F("count") * F("product__price")))["total"])
        context["total_price_with_shipping"] = context['shipping'] + context['total_price']

        return context


def checkout_page(request):
    context = {}
    return render(request, "checkout.html", context)


def contact_page(request):
    context = {}
    return render(request, "contact.html", context)


def detail_page(request):
    context = {}
    return render(request, "detail.html", context)


@login_required(login_url="login")
def delete_cart_item(request: WSGIRequest, pk: int):

    item = get_object_or_404(CartItem, pk=pk)

    if item.user == request.user:
        item.delete()

    return redirect("cart_page")

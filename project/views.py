from typing import Any
from django.shortcuts import render
from django.views import generic

from django.db.models import Q
from django.core.handlers.wsgi import WSGIRequest

from project.forms import ReviewForm

from .models import Category, Product, ProductColor, ProductSize, Review


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

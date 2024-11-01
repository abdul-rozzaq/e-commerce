from django.template import Library
from django.apps import apps

from project.models import Category, Product, ProductColor


register = Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def page_sizes():
    return [4, 8, 12, 16, 20]


@register.simple_tag
def products_count():
    return Product.objects.all().count()

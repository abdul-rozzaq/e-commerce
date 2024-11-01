from django.contrib import admin
from django.utils.html import format_html

from .models import Category, ProductColor, Product, AdditionalInfo, ProductImage, ProductSize, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "view_image"]
    readonly_fields = ["view_image"]

    def view_image(self, obj):
        if obj.image:  # agar rasm bo'lsa
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "Rasm yo'q"


class AdditionalInfoInline(admin.TabularInline):
    model = AdditionalInfo
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "price", "count"]
    list_display_links = ["name"]
    ordering = ("pk",)
    list_per_page = 25

    inlines = [ProductImageInline, AdditionalInfoInline]


admin.site.register(Category)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(Review)

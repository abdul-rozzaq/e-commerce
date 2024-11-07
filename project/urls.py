from django.urls import path

from .views import CheckOutView, DetailPage, HomePageView, SearchProductsView, ShoppingCartView, checkout_page, contact_page, delete_cart_item

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("search/", SearchProductsView.as_view(), name="search_page"),
    path("detail/<int:pk>/", DetailPage.as_view(), name="detail_page"),
    path("cart/", ShoppingCartView.as_view(), name="cart_page"),
    path("checkout/", checkout_page, name="checkout_page"),
    path("add-to-cart/<int:product_id>/", CheckOutView.as_view(), name="add_to_cart"),
    path("delete-cart-item/<int:pk>/", delete_cart_item, name="delete_cart_item"),
    path("contact/", contact_page, name="contact_page"),
]

from django.urls import path


from .views import (
    CheckOutView,
    HomePageView,
    SearchProductsView,
    DetailPage,
    cart_page,
    checkout_page,
    contact_page,
)


urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("search/", SearchProductsView.as_view(), name="search_page"),
    path("detail/<int:pk>/", DetailPage.as_view(), name="detail_page"),
    path("cart/", cart_page, name="cart_page"),
    path("checkout/", checkout_page, name="checkout_page"),
    path("add-to-cart/<int:product_id>/", CheckOutView.as_view(), name="add_to_cart"),
    path("contact/", contact_page, name="contact_page"),
]

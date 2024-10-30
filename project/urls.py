from django.urls import path


from .views import (
    home_page,
    cart_page,
    checkout_page,
    contact_page,
    detail_page,
    shop_page,
    test,
)


urlpatterns = [
    path("", home_page, name="home_page"),
    path("cart/", cart_page, name="cart_page"),
    path("checkout/", checkout_page, name="checkout_page"),
    path("contact/", contact_page, name="contact_page"),
    path("detail/", detail_page, name="detail_page"),
    path("shop/", shop_page, name="shop_page"),
    path("test/", test, name="test_page"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home_page, name="home_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("market/", views.market, name="market"),
    path("market/cart/", views.cart, name="cart"),
    path("market/cart/checkout/", views.checkout, name="checkout"),
    path("market/burger/", views.view_product, name="view_product"),
    path("market/create/product/", views.create_product, name="create_product"),
    path("myProfile/", views.profile, name="profile"),
]
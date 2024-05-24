from django.urls import path

from . import views

app_name = "foodNet"
urlpatterns = [
    # path("", views.test, name="test"),
    path("home", views.home_page, name="home_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("market/", views.market, name="market"),
    path("market/cart/", views.cart, name="cart"),
    path("market/cart/checkout/", views.checkout, name="checkout"),
    path("market/product/<int:product_id>", views.view_product, name="view_product"),
    path("market/create/product/", views.create_product, name="create_product"),
    path("myProfile/<str:prof_name>/<int:prof_id>/", views.profile, name="profile"),
    path("market/search/", views.search, name="search"),
    path("delete/product/<int:product_id>", views.deleteProduct, name="delete_product"),
    path("market/myproduct/<int:product_id>", views.view_own_product, name="view_own_product"),
    path("<str:user_name>/orders", views.orders, name="orders"),


    # API
    path("update_item/", views.updateItem, name="update_item"),
    path("place_order/", views.placeOrder, name="place_order"),
]
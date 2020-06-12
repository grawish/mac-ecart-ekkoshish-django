from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="aboutus"),
    path("contact/", views.contact, name="contactus"),
    path("tracker/", views.tracker, name="tracker"),
    path("products/<int:idx>", views.prod, name="productView"),
    path("search/", views.search, name="ShopHome"),
    path("checkout/", views.checkout, name="ShopHome"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),
    path("cart/", views.cart, name="cart")
]

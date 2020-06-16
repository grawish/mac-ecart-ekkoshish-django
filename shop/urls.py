from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("indexapi/", views.indexapi, name="indexapi"),
    path("about/", views.about, name="aboutus"),
    path("aboutapi/", views.aboutapi, name="aboutusapi"),
    path("contact/", views.contact, name="contactus"),
    path("contactapi/", views.contactapi, name="contactusapi"),
    path("tracker/", views.tracker, name="tracker"),
    path("trackerapi/", views.trackerapi, name="trackerapi"),
    path("products/<int:idx>", views.prod, name="productView"),
    path("productsapi/<int:idx>", views.prodapi, name="productViewapi"),
    path("search/", views.search, name="ShopHome"),
    path("searchapi/", views.searchapi, name="ShopHomeapi"),
    path("checkout/", views.checkout, name="ShopHome"),
    path("checkoutapi/", views.checkoutapi, name="ShopHomeapi"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),
    path("cart/", views.cart, name="cart"),
    path("cartapi/", views.cartapi, name="cartapi"),
]

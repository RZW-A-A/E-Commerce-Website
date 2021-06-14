from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Shophome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("productview/<int:myid>", views.pruductview, name="Showproduct"),
    path("checkout/", views.checkout, name="Checkout"),
    #path("handlerequest/", views.handlerequest, name="HandleRequest")
]

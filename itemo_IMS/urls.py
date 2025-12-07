from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def landing(request):
    return render(request, "landing.html")


def about(request):
    return render(request, "about.html")


def faq(request):
    return render(request, "faq.html")


def contact(request):
    return render(request, "contact.html")


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", landing, name="landing"),
    path("about/", about, name="about"),
    path("faq/", faq, name="faq"),
    path("contact/", contact, name="contact"),

    path("users/", include(("users.urls", "users"), namespace="users")),
    path("store/", include(("store.urls", "store"), namespace="store")),
]

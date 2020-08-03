from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.title, name="title"),
    path("search/<str:title>/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("rand/", views.rand, name="rand")
]

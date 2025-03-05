from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create/", views.createPage, name="createPage"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("random/", views.randomPage, name="randomPage"),
]

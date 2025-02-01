from django.urls import path

from . import views

urlpatterns = [
    # home page
    path("", views.index, name="index"),
    # entry page
    path("wiki/<str:title>", views.entry_pages, name="entry_page"),
    # search page
    path("search", views.search, name="search"),
    # new page
    path("new", views.new, name="new_page"),
    # edit page
    path("edit/<str:title>", views.edit, name="edit_page"),
    # random page
    path("random", views.random_page, name="random_page")

]

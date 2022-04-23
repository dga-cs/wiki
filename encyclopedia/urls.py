from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.entry_page, name="entry_page"),
    path("add", views.add, name="add"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("wiki/edit/<str:entry_title>", views.edit_entry, name="edit_entry"),
    path("save_ed_entry", views.save_ed_entry, name="save_ed_entry"),
]

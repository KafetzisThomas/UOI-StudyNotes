from django.urls import path
from . import views

app_name = "notes"
urlpatterns = [
    path("", views.notes, name="notes"),
    path("note/<int:note_id>/", views.note, name="note"),
    path("note/<int:note_id>/like_note/", views.like_note, name="like_note"),
    path("note/new/", views.new_note, name="new_note"),
    path("note/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("note/<int:note_id>/delete/", views.delete_note, name="delete_note"),
]

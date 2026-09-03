from django.urls import path
from . import views

app_name = "notes"
urlpatterns = [
    path("", views.display_notes, name="display_notes"),
    path("note/<int:note_id>/", views.note, name="note"),
    path("note/<int:note_id>/like_note", views.like_note, name="like_note"),
    path("new_note/", views.new_note, name="new_note"),
    path("edit_note/<int:note_id>/", views.edit_note, name="edit_note"),
    path("edit_note/<int:note_id>/delete", views.delete_note, name="delete_note"),
]

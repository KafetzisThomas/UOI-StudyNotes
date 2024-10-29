"""Defines URL patterns for notes"""

from django.urls import path
from . import views

app_name = "notes"
urlpatterns = [
    # Notes page
    path("", views.display_notes, name="display_notes"),
    # Note page
    path("note/<int:note_id>/", views.note, name="note"),
    # Like note page
    path("note/<int:note_id>/like_note", views.like_note, name="like_note"),
    # Create a new note page
    path("new_note/", views.new_note, name="new_note"),
    # Edit note page
    path("edit_note/<int:note_id>/", views.edit_note, name="edit_note"),
    # Delete note page
    path("edit_note/<int:note_id>/delete", views.delete_note, name="delete_note"),
]

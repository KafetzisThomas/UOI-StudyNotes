"""Defines URL patterns for forum"""

from django.urls import path
from . import views

app_name = "forum"
urlpatterns = [
    # Posts page
    path("", views.display_posts, name="display_posts"),
    # Create a new post page
    path("new_post/", views.new_post, name="new_post"),
]

"""Defines URL patterns for forum"""

from django.urls import path
from . import views

app_name = "forum"
urlpatterns = [
    # Posts page
    path("", views.display_posts, name="display_posts")
]

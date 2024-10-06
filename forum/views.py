from django.shortcuts import render
from .models import Post


def display_posts(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "forum/posts.html", context)

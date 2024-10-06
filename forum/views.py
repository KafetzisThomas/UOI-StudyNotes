from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post


def display_posts(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "forum/posts.html", context)


def new_post(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("forum:display_posts")
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, "forum/new_post.html", context)

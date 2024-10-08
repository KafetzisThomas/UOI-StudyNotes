from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post


def display_posts(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "forum/posts.html", context)


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {"post": post}
    return render(request, "forum/post.html", context)


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


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("forum:display_posts")
    else:
        initial_data = {"title": post.title, "content": post.content}
        form = PostForm(instance=post, initial=initial_data)

    context = {"post": post, "form": form}
    return render(request, "forum/edit_post.html", context)

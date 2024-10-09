from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import PostForm, CommentForm
from .models import Post, Comment


def display_posts(request):
    posts = Post.objects.all().order_by("-timestamp")
    context = {"posts": posts}
    return render(request, "forum/posts.html", context)


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("forum:post", post_id=post_id)
    else:
        form = CommentForm()

    context = {"form": form, "post": post, "comments": comments}
    return render(request, "forum/post.html", context)


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)
        obj = form.save(commit=False)
        if form.is_valid():
            obj.user = request.user
            form.save()
            return redirect("forum:display_posts")
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, "forum/new_post.html", context)


@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user != request.user:
        raise Http404

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from .utils import send_reply_notification
from .forms import PostForm, ReplyForm
from .models import Post, TOPICS


def display_posts(request):
    # Retrieve selected topic & search query,
    # from the query parameters
    topic = request.GET.get("topic")
    search_query = request.GET.get("search_query")
    posts = Post.objects.all().order_by("-timestamp")

    # Filter posts by search query in the title if provided
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    # Filter posts by topic if a topic is selected
    if topic:
        posts = posts.filter(topic=topic)

    paginator = Paginator(posts, 10)  # Display 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "TOPICS": TOPICS, "search_query": search_query}
    return render(request, "forum/posts.html", context)


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all()

    # Like functionality
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes()

    if request.method == "POST":
        form = ReplyForm(data=request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.save()
            post_url = reverse("forum:post", args=[post.id])
            if new_reply.user != post.user:
                send_reply_notification(
                    sender=new_reply.user,
                    receiver=post.user,
                    post_url=post_url,
                    reply=new_reply,
                )
            return redirect("forum:post", post_id=post_id)
    else:
        form = ReplyForm()

    context = {
        "form": form,
        "post": post,
        "replies": replies,
        "number_of_likes": number_of_likes,
        "post_is_liked": liked,
    }
    return render(request, "forum/post.html", context)


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse("forum:post", args=[post_id]))


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            form.save()
            messages.success(request, "Post created successfully.")
            return redirect("forum:display_posts")
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, "forum/new_post.html", context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        raise Http404

    if request.method == "POST":
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Post modified successfully.")
            return redirect("forum:post", post_id=post_id)
    else:
        initial_data = {"title": post.title, "content": post.content}
        form = PostForm(instance=post, initial=initial_data)

    context = {"post": post, "form": form}
    return render(request, "forum/edit_post.html", context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        raise Http404
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect("forum:display_posts")

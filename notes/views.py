from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from .utils import send_comment_notification
from .forms import NoteForm, CommentForm
from .models import Note, DEPARTMENTS


def display_notes(request):
    # Retrieve selected department & search query,
    # from the query parameters
    department = request.GET.get("department")
    search_query = request.GET.get("search_query")
    notes = Note.objects.all().order_by("-timestamp")

    # Filter notes by search query in the title if provided
    if search_query:
        notes = notes.filter(title__icontains=search_query)

    # Filter notess by department if a department is selected
    if department:
        notes = notes.filter(department=department)

    paginator = Paginator(notes, 10)  # Display 10 notes per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "DEPARTMENTS": DEPARTMENTS,
        "search_query": search_query,
    }
    return render(request, "notes/notes.html", context)


def note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    comments = note.comments.all()

    # Like functionality
    liked = False
    if note.likes.filter(id=request.user.id).exists():
        liked = True
    number_of_likes = note.number_of_likes()

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.note = note
            new_comment.save()
            note_url = reverse("notes:note", args=[note.id])
            if not settings.DEBUG and new_comment.user != note.user:
                send_comment_notification(
                    sender=new_comment.user,
                    receiver=note.user,
                    note_url=note_url,
                    comment=new_comment,
                )
            return redirect("notes:note", note_id=note_id)
    else:
        form = CommentForm()

    context = {
        "form": form,
        "note": note,
        "comments": comments,
        "number_of_likes": number_of_likes,
        "note_is_liked": liked,
    }
    return render(request, "notes/note.html", context)


def like_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.likes.filter(id=request.user.id).exists():
        note.likes.remove(request.user)
    else:
        note.likes.add(request.user)

    return HttpResponseRedirect(reverse("notes:note", args=[note_id]))


@login_required
def new_note(request):
    if request.method == "POST":
        form = NoteForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            form.save()
            messages.success(request, "Note created successfully.")
            return redirect("notes:display_notes")
    else:
        form = NoteForm()

    context = {"form": form}
    return render(request, "notes/new_note.html", context)


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        raise Http404

    if request.method == "POST":
        form = NoteForm(instance=note, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Note modified successfully.")
            return redirect("notes:note", note_id=note_id)
    else:
        initial_data = {"title": note.title, "content": note.content}
        form = NoteForm(instance=note, initial=initial_data)

    context = {"note": note, "form": form}
    return render(request, "notes/edit_note.html", context)


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        raise Http404
    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect("notes:display_notes")

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse
from .models import Note, DEPARTMENTS
from .forms import NoteForm, CommentForm
from .utils import send_comment_notification

def notes(request):
    department = request.GET.get("department")
    search = request.GET.get("search")

    notes = Note.objects.all().order_by("-timestamp")

    if search:
        notes = notes.filter(title__icontains=search)

    if department:
        notes = notes.filter(department=department)

    paginator = Paginator(notes, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {"departments": DEPARTMENTS, "search": search, "page": page}
    return render(request, "notes/notes.html", context)

def note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    comments = note.comments.all()

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
                send_comment_notification(new_comment.user, note.user, note_url, new_comment)

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

@login_required
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
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            form.save()
            messages.success(request, "Note created successfully.")
            return redirect("notes:notes")
    else:
        form = NoteForm()

    return render(request, "notes/new_note.html", {"form": form})

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note modified successfully.")
            return redirect("notes:note", note_id=note_id)
    else:
        initial_data = {"title": note.title, "content": note.content}
        form = NoteForm(instance=note, initial=initial_data)

    context = {"form": form, "note": note}
    return render(request, "notes/edit_note.html", context)

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect("notes:notes")

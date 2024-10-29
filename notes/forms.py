from django import forms
from .models import Note, Comment, DEPARTMENTS


class NoteForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 1}
        ),
        required=True,
    )
    department = forms.ChoiceField(
        label="Department",
        choices=DEPARTMENTS,
        widget=forms.Select(attrs={"class": "form-control bg-dark text-light"}),
        required=True,
    )
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 10}
        ),
        required=True,
    )

    class Meta:
        model = Note
        fields = ["title", "department", "content"]


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="Write your comment here ",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 10}
        ),
        required=True,
    )

    class Meta:
        model = Comment
        fields = ["content"]

from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Note, Comment, DEPARTMENTS


class NoteForm(forms.ModelForm):
    department = forms.ChoiceField(label="Department", choices=DEPARTMENTS)
    content = forms.CharField(label="Content", widget=SummernoteWidget(), required=True)

    class Meta:
        model = Note
        fields = ["title", "department", "subject", "content", "file"]


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="Write your comment here", widget=forms.Textarea(attrs={"rows": 10}), required=True)

    class Meta:
        model = Comment
        fields = ["content"]

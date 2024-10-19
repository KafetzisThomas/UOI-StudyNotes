from django import forms
from .models import Post, Reply, TOPICS


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 1}
        ),
        required=True,
    )
    topic = forms.ChoiceField(
        label="Topic",
        choices=TOPICS,
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
        model = Post
        fields = ["title", "topic", "content"]


class ReplyForm(forms.ModelForm):
    content = forms.CharField(
        label="Write your reply here ",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 10}
        ),
        required=True,
    )

    class Meta:
        model = Reply
        fields = ["content"]

from django import forms
from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "topic", "content"]
        widgets = {
            "title": forms.Textarea(
                attrs={"style": "background-color: #2c3035; color: #adb5bd;", "rows": 1}
            ),
            "topic": forms.Select(
                attrs={"style": "background-color: #2c3035; color: #adb5bd;"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "custom-textarea",
                    "style": "background-color: #2c3035; color: #adb5bd;",
                    "rows": 10,
                    "placeholder": "Write your reply here...",
                }
            ),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "custom-textarea",
                    "style": "background-color: #2c3035; color: #adb5bd;",
                    "rows": 10,
                    "placeholder": "Write your reply here...",
                }
            ),
        }

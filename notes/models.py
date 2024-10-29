from django.db import models
from django.contrib.auth.models import User

DEPARTMENTS = (
    ("Philosophy", "Philosophy"),
    ("Sciences", "Sciences"),
    ("Health Sciences", "Health Sciences"),
    ("Education", "Education"),
    ("Fine Arts", "Fine Arts"),
    ("Engineering", "Engineering"),
    ("Social Sciences", "Social Sciences"),
    ("Economics and Administrative Sciences", "Economics and Administrative Sciences"),
    ("Music Studies", "Music Studies"),
    ("Informatics and Telecommunications", "Informatics and Telecommunications"),
    ("Agricultural Technology", "Agricultural Technology"),
)


class Note(models.Model):
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=DEPARTMENTS, default=None)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_notes")
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:10]

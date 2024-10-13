from django.db import models
from django.contrib.auth.models import User

TOPICS = (
    ("Software", "Software"),
    ("Hardware", "Hardware"),
    ("Operating Systems", "Operating Systems"),
    ("Networking", "Networking"),
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=100, choices=TOPICS, default=None)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="like_post")
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:10]

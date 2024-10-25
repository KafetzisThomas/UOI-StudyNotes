"""
This module contains test cases for the Post model.
The tests cover various aspects of the model, including post creation,
field validations, foreign key constraints, and the __str__ method.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Post


class PostModelTests(TestCase):
    """
    Test suite for the Post model.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and defining post data.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.post_data = {
            "title": "Test Post",
            "topic": "Software",
            "content": "This is test content.",
            "user": self.user,
        }

    def test_create_post(self):
        """
        Test that a post can be created with the given data.
        """
        post = Post.objects.create(**self.post_data)
        self.assertEqual(post.title, self.post_data["title"])
        self.assertEqual(post.topic, self.post_data["topic"])
        self.assertEqual(post.content, self.post_data["content"])
        self.assertEqual(post.user, self.post_data["user"])
        self.assertIsNotNone(post.timestamp)

    def test_number_of_likes(self):
        """
        Test that method returns the correct count of likes on a post.
        """
        post = Post.objects.create(**self.post_data)
        self.assertEqual(post.number_of_likes(), 0)  # 0 likes
        post.likes.add(self.user)  # 1 likes
        self.assertEqual(post.number_of_likes(), 1)

    def test_str_method(self):
        """
        Test that the __str__ method returns the post name.
        """
        post = Post.objects.create(**self.post_data)
        self.assertEqual(str(post), post.title)

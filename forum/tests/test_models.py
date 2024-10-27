"""
This module contains test cases for the Post & Reply models.
The tests cover various aspects of the model, including post & reply creation,
field validations, foreign key constraints, and the __str__ method.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Post, Reply


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


class ReplyModelTests(TestCase):
    """
    Test suite for the Reply model.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user, a post & a reply.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            topic="Software",
            content="This is test content.",
            user=self.user,
        )
        self.reply_data = {
            "post": self.post,
            "user": self.user,
            "content": "This is a test reply content.",
        }

    def test_create_reply(self):
        """
        Test that a reply can be created with the given data.
        """
        reply = Reply.objects.create(**self.reply_data)
        self.assertEqual(reply.post, self.reply_data["post"])
        self.assertEqual(reply.user, self.reply_data["user"])
        self.assertEqual(reply.content, self.reply_data["content"])
        self.assertIsNotNone(reply.timestamp)

    def test_str_method(self):
        """
        Test that the __str__ method returns the first 10 characters
        of the reply content.
        """
        reply = Reply.objects.create(**self.reply_data)
        self.assertEqual(str(reply), self.reply_data["content"][:10])

    def test_reply_relationship_with_post(self):
        """
        Test that a reply is associated with the correct post,
        and can be accessed via the post's replies.
        """
        reply = Reply.objects.create(**self.reply_data)
        self.assertIn(reply, self.post.replies.all())

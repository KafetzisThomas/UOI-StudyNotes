"""
This module contains test cases for the following views:
* display_posts
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post


class DisplayPostsViewTests(TestCase):
    """
    Test suite for the display_posts view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and sample posts,
        with different topics and titles.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.posts = [
            Post.objects.create(
                title="Post 1",
                topic="Software",
                content="Test content 1",
                user=self.user,
            ),
            Post.objects.create(
                title="Post 2",
                topic="Hardware",
                content="Test content 2",
                user=self.user,
            ),
            Post.objects.create(
                title="Post 3",
                topic="Networking",
                content="Test content 3",
                user=self.user,
            ),
        ]

    def test_display_posts_view_status_code(self):
        """
        Test that the view returns a 200 status code.
        """
        response = self.client.get(reverse("forum:display_posts"))
        self.assertEqual(response.status_code, 200)

    def test_display_posts_view_template(self):
        """
        Test that the view uses the correct template.
        """
        response = self.client.get(reverse("forum:display_posts"))
        self.assertTemplateUsed(response, "forum/posts.html")

    def test_filter_posts_by_topic(self):
        """
        Test that the view filters posts by the selected topic.
        """
        response = self.client.get(
            reverse("forum:display_posts"), {"topic": "Software"}
        )
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_filter_posts_by_search_query(self):
        """
        Test that the view filters posts by a search query in the title.
        """
        response = self.client.get(
            reverse("forum:display_posts"), {"search_query": "Post 2"}
        )
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_pagination(self):
        """
        Test that the view paginates posts, displaying a maximum of 10 per page.
        """
        # Create additional posts to trigger pagination
        for i in range(9):
            Post.objects.create(
                title=f"Test Post {i}",
                topic="Software",
                content="Test post content",
                user=self.user,
            )

        # Check 1st page, should have 10 posts
        response = self.client.get(reverse("forum:display_posts"))
        self.assertEqual(len(response.context["page_obj"]), 10)

        # Check 2nd page, should have 2 posts
        response = self.client.get(reverse("forum:display_posts"), {"page": 2})
        self.assertEqual(len(response.context["page_obj"]), 2)

"""
This module contains test cases for the following views:
* display_posts, post, new_post, edit_post
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


class PostViewTests(TestCase):
    """
    Test suite for the post view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user & a post.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            topic="Software",
            content="Test content",
            user=self.user,
        )
        self.url = reverse("forum:post", args=[self.post.id])
        self.client.login(username="testuser", password="password123")

    def test_post_view_status_code(self):
        """
        Test that the view returns a 200 status code for an existing post.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_view_template(self):
        """
        Test that the view uses the correct template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "forum/post.html")

    def test_post_view_context_data(self):
        """
        Test that the view passes the correct context data to the template.
        """
        response = self.client.get(self.url)
        self.assertIn("post", response.context)
        self.assertIn("form", response.context)
        self.assertIn("replies", response.context)
        self.assertIn("number_of_likes", response.context)
        self.assertIn("post_is_liked", response.context)

    def test_like_status_in_context(self):
        """
        Test that the 'post_is_liked' context variable is True,
        if the user has liked the post.
        """
        self.post.likes.add(self.user)
        response = self.client.get(self.url)
        self.assertTrue(response.context["post_is_liked"])

    def test_number_of_likes_in_context(self):
        """
        Test that the 'number_of_likes' context variable
        reflects the correct number of likes.
        """
        self.post.likes.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["number_of_likes"], 1)

    def test_reply_submission(self):
        """
        Test that submitting a valid reply form adds a new reply to the post.
        """
        self.client.post(self.url, {"content": "This is a test reply"})
        self.assertEqual(self.post.replies.count(), 1)


class NewPostViewTests(TestCase):
    """
    Test suite for the new_post view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.url = reverse("forum:new_post")

    def test_new_post_view_status_code(self):
        """
        Test that the new_post view returns a 200 status code
        for authenticated users.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_new_post_view_redirect_if_not_logged_in(self):
        """
        Test that the view redirects to the login page
        if the user is not authenticated.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('users:login')}?next={self.url}")

    def test_new_post_view_template(self):
        """
        Test that the view uses the correct template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "forum/new_post.html")

    def test_post_creation_success(self):
        """
        Test that a post is created successfully when valid data is submitted.
        """
        post_data = {
            "title": "Test Post",
            "topic": "Software",
            "content": "This is a test post content.",
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().user, self.user)  # authenticated user
        self.assertRedirects(response, reverse("forum:display_posts"))

    def test_invalid_post_data(self):
        """
        Test that invalid form data does not create a post.
        """
        post_data = {
            "title": "",  # Invalid: title is required
            "topic": "Hardware",
            "content": "Content without a title.",
        }
        self.client.post(self.url, post_data)
        self.assertEqual(Post.objects.count(), 0)


class EditPostViewTests(TestCase):
    """
    Test suite for the edit_post view.
    """

    def setUp(self):
        """
        Set up the test environment by creating users & a post.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="testuser2@example.com", password="password456"
        )
        self.post = Post.objects.create(
            title="Original Title",
            topic="Software",
            content="Original content.",
            user=self.user,
        )
        self.url = reverse("forum:edit_post", args=[self.post.id])
        self.client.login(username="testuser", password="password123")

    def test_edit_post_success(self):
        """
        Test that the post is successfully edited with valid data.
        """
        updated_data = {
            "title": "Updated Title",
            "topic": "Software",
            "content": "Updated content.",
        }
        response = self.client.post(self.url, updated_data)
        self.post.refresh_from_db()

        self.assertEqual(self.post.title, updated_data["title"])
        self.assertEqual(self.post.content, updated_data["content"])
        self.assertRedirects(response, reverse("forum:post", args=[self.post.id]))

    def test_edit_post_permission_denied(self):
        """
        Test that a user who is not the owner of the post receives a 404 error.
        """
        self.client.logout()
        self.client.login(username="testuser2", password="password456")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_edit_post_invalid_data(self):
        """
        Test that invalid form data does not save the form.
        """
        invalid_data = {
            "title": "",  # Invalid: title is required
            "topic": "Software",
            "content": "Updated content.",
        }
        self.client.post(self.url, invalid_data)

        # Ensure post data remains unchanged
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Original Title")
        self.assertEqual(self.post.content, "Original content.")

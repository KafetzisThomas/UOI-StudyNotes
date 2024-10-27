"""
This module contains test cases for the following classes:
* PostForm (validation)
* ReplyForm (validation)
"""

from django.test import TestCase
from ..forms import PostForm, ReplyForm
from ..models import TOPICS


class PostFormTests(TestCase):
    """
    Test suite for the PostForm.
    """

    def setUp(self):
        """
        Set up the test environment by creating a test post.
        """
        self.post_data = {
            "title": "Test Post",
            "topic": TOPICS[0][0],  # "Software" topic
            "content": "This is test content.",
        }

    def test_post_form_valid(self):
        """
        Test that the form is valid with correct data.
        """
        form = PostForm(data=self.post_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_post_form_missing_fields(self):
        """
        Test that the form is invalid if required fields are missing.
        """
        # Test missing title
        data = self.post_data.copy()
        data.pop("title")
        form = PostForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing topic
        data = self.post_data.copy()
        data.pop("topic")
        form = PostForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing content
        data = self.post_data.copy()
        data.pop("content")
        form = PostForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)


class ReplyFormTests(TestCase):
    """
    Test suite for the ReplyForm.
    """

    def setUp(self):
        """
        Set up the test environment by creating a test reply.
        """
        self.reply_data = {"content": "This is a test reply content."}

    def test_reply_form_valid(self):
        """
        Test that the form is valid with correct data.
        """
        form = ReplyForm(data=self.reply_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_reply_form_missing_field(self):
        """
        Test that the form is invalid if the content field is missing.
        """
        form = ReplyForm(data={})
        self.assertFalse(form.is_valid(), form.errors)

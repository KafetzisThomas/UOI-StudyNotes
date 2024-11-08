"""
This module contains test cases for the following classes:
* NoteForm (validation)
* CommentForm (validation)
"""

from django.test import TestCase
from ..forms import NoteForm, CommentForm
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import DEPARTMENTS


class NoteFormTests(TestCase):
    """
    Test suite for the NoteForm.
    """

    def setUp(self):
        """
        Set up the test environment by creating a test note.
        """
        self.note_data = {
            "title": "Test Note",
            "department": DEPARTMENTS[0][0],  # "Philosophy" department
            "subject": "Modern Philosophy",
            "content": "This is test content.",
            "file": SimpleUploadedFile("testfile.txt", b"File content."),
        }

    def test_note_form_valid(self):
        """
        Test that the form is valid with correct data.
        """
        form = NoteForm(data=self.note_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_note_form_missing_fields(self):
        """
        Test that the form is invalid if required fields are missing.
        """
        # Test missing title
        data = self.note_data.copy()
        data.pop("title")
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing deparrtment
        data = self.note_data.copy()
        data.pop("department")
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing subject
        data = self.note_data.copy()
        data.pop("subject")
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing content
        data = self.note_data.copy()
        data.pop("content")
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)


class CommentFormTests(TestCase):
    """
    Test suite for the CommentForm.
    """

    def setUp(self):
        """
        Set up the test environment by creating a test comment.
        """
        self.comment_data = {"content": "This is a test comment."}

    def test_comment_form_valid(self):
        """
        Test that the form is valid with correct data.
        """
        form = CommentForm(data=self.comment_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_comment_form_missing_field(self):
        """
        Test that the form is invalid if the content field is missing.
        """
        form = CommentForm(data={})
        self.assertFalse(form.is_valid(), form.errors)

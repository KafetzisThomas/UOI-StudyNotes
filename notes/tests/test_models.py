"""
This module contains test cases for the Note & Comment models.
The tests cover various aspects of the model, including note & comment creation,
field validations, foreign key constraints, and the __str__ method.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Note, Comment


class NoteModelTests(TestCase):
    """
    Test suite for the Note model.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and defining note data.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@uoi.gr", password="password123"
        )
        self.note_data = {
            "title": "Test Note",
            "department": "Philosophy",
            "subject": "Modern Philosophy",
            "content": "This is test content.",
            "file": SimpleUploadedFile("testfile.txt", b"File content."),
            "user": self.user,
        }

    def test_create_note(self):
        """
        Test that a note can be created with the given data.
        """
        note = Note.objects.create(**self.note_data)
        self.assertEqual(note.title, self.note_data["title"])
        self.assertEqual(note.department, self.note_data["department"])
        self.assertEqual(note.subject, self.note_data["subject"])
        self.assertEqual(note.content, self.note_data["content"])
        self.assertTrue(note.file.name.startswith("uploads/"))
        self.assertEqual(note.file.read(), b"File content.")
        self.assertEqual(note.user, self.note_data["user"])
        self.assertIsNotNone(note.timestamp)

    def test_number_of_likes(self):
        """
        Test that method returns the correct count of likes on a note.
        """
        note = Note.objects.create(**self.note_data)
        self.assertEqual(note.number_of_likes(), 0)  # 0 likes
        note.likes.add(self.user)  # 1 likes
        self.assertEqual(note.number_of_likes(), 1)

    def test_str_method(self):
        """
        Test that the __str__ method returns the note name.
        """
        note = Note.objects.create(**self.note_data)
        self.assertEqual(str(note), note.title)


class CommentModelTests(TestCase):
    """
    Test suite for the Comment model.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user, a note & a comment.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@uoi.gr", password="password123"
        )
        self.note = Note.objects.create(
            title="Test Note",
            department="Philosophy",
            subject="Modern Philosophy",
            content="This is test content.",
            file=SimpleUploadedFile("testfile.txt", b"File content."),
            user=self.user,
        )
        self.comment_data = {
            "note": self.note,
            "user": self.user,
            "content": "This is a test comment.",
        }

    def test_create_comment(self):
        """
        Test that a comment can be created with the given data.
        """
        comment = Comment.objects.create(**self.comment_data)
        self.assertEqual(comment.note, self.comment_data["note"])
        self.assertEqual(comment.user, self.comment_data["user"])
        self.assertEqual(comment.content, self.comment_data["content"])
        self.assertIsNotNone(comment.timestamp)

    def test_str_method(self):
        """
        Test that the __str__ method returns the first 10 characters
        of the comment content.
        """
        comment = Comment.objects.create(**self.comment_data)
        self.assertEqual(str(comment), self.comment_data["content"][:10])

    def test_comment_relationship_with_note(self):
        """
        Test that a comment is associated with the correct note,
        and can be accessed via the note's comments.
        """
        comment = Comment.objects.create(**self.comment_data)
        self.assertIn(comment, self.note.comments.all())

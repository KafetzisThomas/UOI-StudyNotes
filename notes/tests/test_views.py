"""
This module contains test cases for the following views:
* display_notes, note, new_note, edit_note, delete_note
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Note


class DisplayNotesViewTests(TestCase):
    """
    Test suite for the display_notes view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and sample notes,
        with different departments, subjects and titles.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@uoi.gr", password="password123"
        )
        self.notes = [
            Note.objects.create(
                title="Note 1",
                department="Philosophy",
                subject="Modern Philosophy",
                content="Test content 1",
                user=self.user,
            ),
            Note.objects.create(
                title="Note 2",
                department="Informatics and Telecommunications",
                subject="Programming",
                content="Test content 2",
                user=self.user,
            ),
            Note.objects.create(
                title="Note 3",
                department="Health Sciences",
                subject="Physiology",
                content="Test content 3",
                user=self.user,
            ),
        ]

    def test_display_notes_view_status_code(self):
        """
        Test that the view returns a 200 status code.
        """
        response = self.client.get(reverse("notes:display_notes"))
        self.assertEqual(response.status_code, 200)

    def test_display_notes_view_template(self):
        """
        Test that the view uses the correct template.
        """
        response = self.client.get(reverse("notes:display_notes"))
        self.assertTemplateUsed(response, "notes/notes.html")

    def test_filter_notes_by_department(self):
        """
        Test that the view filters notes by the selected department.
        """
        response = self.client.get(
            reverse("notes:display_notes"), {"department": "Philosophy"}
        )
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_filter_notes_by_search_query(self):
        """
        Test that the view filters notes by a search query in the title.
        """
        response = self.client.get(
            reverse("notes:display_notes"), {"search_query": "Note 2"}
        )
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_pagination(self):
        """
        Test that the view paginates notes, displaying a maximum of 10 per page.
        """
        # Create additional notes to trigger pagination
        for i in range(9):
            Note.objects.create(
                title=f"Test Note {i}",
                department="Philosophy",
                subject="Modern Philosophy",
                content="Test note content",
                user=self.user,
            )

        # Check 1st page, should have 10 notes
        response = self.client.get(reverse("notes:display_notes"))
        self.assertEqual(len(response.context["page_obj"]), 10)

        # Check 2nd page, should have 2 notes
        response = self.client.get(reverse("notes:display_notes"), {"page": 2})
        self.assertEqual(len(response.context["page_obj"]), 2)


class NoteViewTests(TestCase):
    """
    Test suite for the note view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user & a note.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@uoi.gr", password="password123"
        )
        self.note = Note.objects.create(
            title="Test Note",
            department="Philosophy",
            subject="Modern Philosophy",
            content="Test content",
            user=self.user,
        )
        self.url = reverse("notes:note", args=[self.note.id])
        self.client.login(username="testuser", password="password123")

    def test_note_view_status_code(self):
        """
        Test that the view returns a 200 status code for an existing note.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_note_view_template(self):
        """
        Test that the view uses the correct template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "notes/note.html")

    def test_note_view_context_data(self):
        """
        Test that the view passes the correct context data to the template.
        """
        response = self.client.get(self.url)
        self.assertIn("note", response.context)
        self.assertIn("form", response.context)
        self.assertIn("comments", response.context)
        self.assertIn("number_of_likes", response.context)
        self.assertIn("note_is_liked", response.context)

    def test_like_status_in_context(self):
        """
        Test that the 'note_is_liked' context variable is True,
        if the user has liked the note.
        """
        self.note.likes.add(self.user)
        response = self.client.get(self.url)
        self.assertTrue(response.context["note_is_liked"])

    def test_number_of_likes_in_context(self):
        """
        Test that the 'number_of_likes' context variable
        reflects the correct number of likes.
        """
        self.note.likes.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["number_of_likes"], 1)

    def test_comment_submission(self):
        """
        Test that submitting a valid comment form adds a new comment to the note.
        """
        self.client.post(self.url, {"content": "This is a test comment."})
        self.assertEqual(self.note.comments.count(), 1)


class NewNoteViewTests(TestCase):
    """
    Test suite for the new_note view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@uoi.gr", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.url = reverse("notes:new_note")

    def test_new_note_view_status_code(self):
        """
        Test that the new_note view returns a 200 status code
        for authenticated users.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_new_note_view_redirect_if_not_logged_in(self):
        """
        Test that the view redirects to the login page
        if the user is not authenticated.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('users:login')}?next={self.url}")

    def test_new_note_view_template(self):
        """
        Test that the view uses the correct template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "notes/new_note.html")

    def test_note_creation_success(self):
        """
        Test that a note is created successfully when valid data is submitted.
        """
        note_data = {
            "title": "Test Note",
            "department": "Philosophy",
            "subject": "Modern Philosophy",
            "content": "This is a test note content.",
        }
        response = self.client.post(self.url, note_data)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().user, self.user)  # authenticated user
        self.assertRedirects(response, reverse("notes:display_notes"))

    def test_invalid_note_data(self):
        """
        Test that invalid form data does not create a note.
        """
        note_data = {
            "title": "",  # Invalid: title is required
            "department": "Philosophy",
            "subject": "Modern Philosophy",
            "content": "This is a test note content.",
        }
        self.client.post(self.url, note_data)
        self.assertEqual(Note.objects.count(), 0)


class EditNoteViewTests(TestCase):
    """
    Test suite for the edit_note view.
    """

    def setUp(self):
        """
        Set up the test environment by creating users & a note.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@uoi.gr", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="testuser2@uoi.gr", password="password456"
        )
        self.note = Note.objects.create(
            title="Original Title",
            department="Philosophy",
            subject="Modern Philosophy",
            content="Original content.",
            user=self.user,
        )
        self.url = reverse("notes:edit_note", args=[self.note.id])
        self.client.login(username="testuser", password="password123")

    def test_edit_note_success(self):
        """
        Test that the note is successfully edited with valid data.
        """
        updated_data = {
            "title": "Updated Title",
            "department": "Fine Arts",
            "subject": "Printmaking",
            "content": "Updated content.",
        }
        response = self.client.post(self.url, updated_data)
        self.note.refresh_from_db()

        self.assertEqual(self.note.title, updated_data["title"])
        self.assertEqual(self.note.department, updated_data["department"])
        self.assertEqual(self.note.subject, updated_data["subject"])
        self.assertEqual(self.note.content, updated_data["content"])
        self.assertRedirects(response, reverse("notes:note", args=[self.note.id]))

    def test_edit_note_permission_denied(self):
        """
        Test that a user who is not the owner of the note receives a 404 error.
        """
        self.client.logout()
        self.client.login(username="testuser2", password="password456")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_edit_note_invalid_data(self):
        """
        Test that invalid form data does not save the form.
        """
        invalid_data = {
            "title": "",  # Invalid: title is required
            "department": "Fine Arts",
            "subject": "Printmaking",
            "content": "Updated content.",
        }
        self.client.post(self.url, invalid_data)

        # Ensure note data remains unchanged
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Original Title")
        self.assertEqual(self.note.content, "Original content.")


class DeleteNoteViewTests(TestCase):
    """
    Test suite for the delete_note view.
    """

    def setUp(self):
        """
        Set up the test environment by creating users & a note.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@uoi.gr", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="testuser2@uoi.gr", password="password456"
        )
        self.note = Note.objects.create(
            title="Test Note",
            department="Philosophy",
            subject="Modern Philosophy",
            content="Test note content.",
            user=self.user,
        )
        self.url = reverse("notes:delete_note", args=[self.note.id])
        self.client.login(username="testuser", password="password123")

    def test_delete_note_successful(self):
        """
        Test that a note is deleted successfully when the owner requests deletion.
        """
        response = self.client.post(self.url)

        # Check the note no longer exists
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
        self.assertRedirects(response, reverse("notes:display_notes"))

    def test_delete_note_non_owner(self):
        """
        Test that a non-owner attempting to delete a note receives a 404 error.
        """
        self.client.logout()
        self.client.login(username="testuser2", password="password456")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

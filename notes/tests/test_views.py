from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Note

User = get_user_model()


class NotesViewTests(TestCase):

    def setUp(self):
        self.url = reverse("notes:notes")
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.notes = [
            Note.objects.create(
                title="Note 1",
                department="Philosophy",
                subject="Modern Philosophy",
                content="Test content 1",
                file=SimpleUploadedFile("testfile1.txt", b"File 1 content."),
                user=self.user,
            ),
            Note.objects.create(
                title="Note 2",
                department="Informatics and Telecommunications",
                subject="Programming",
                content="Test content 2",
                file=SimpleUploadedFile("testfile2.txt", b"File 2 content."),
                user=self.user,
            ),
            Note.objects.create(
                title="Note 3",
                department="Health Sciences",
                subject="Physiology",
                content="Test content 3",
                file=SimpleUploadedFile("testfile3.txt", b"File 3 content."),
                user=self.user,
            ),
        ]

    def test_filter_notes_by_department(self):
        response = self.client.get(self.url, {"department": "Philosophy"})
        self.assertEqual(len(response.context["page"]), 1)

    def test_filter_notes_by_search_query(self):
        response = self.client.get(self.url, {"search": "Note 2"})
        self.assertEqual(len(response.context["page"]), 1)

    def test_pagination(self):
        for i in range(9):
            Note.objects.create(
                title=f"Test Note {i}",
                department="Philosophy",
                subject="Modern Philosophy",
                content="Test note content",
                user=self.user,
            )

        # 1st page = 10 notes
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["page"]), 10)

        # 2nd page = 2 notes
        response = self.client.get(self.url, {"page": 2})
        self.assertEqual(len(response.context["page"]), 2)


class NoteViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.note = Note.objects.create(
            title="Test Note",
            department="Philosophy",
            subject="Modern Philosophy",
            content="Test content",
            file=SimpleUploadedFile("testfile.txt", b"File content."),
            user=self.user,
        )
        self.url = reverse("notes:note", args=[self.note.id])
        self.client.login(username="user", password="Str0ng_p@ssword")

    def test_note_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("note", response.context)
        self.assertIn("form", response.context)
        self.assertIn("comments", response.context)
        self.assertIn("number_of_likes", response.context)
        self.assertIn("note_is_liked", response.context)

    def test_like_status_and_number_in_context(self):
        self.note.likes.add(self.user)
        response = self.client.get(self.url)
        self.assertTrue(response.context["note_is_liked"])
        self.assertEqual(response.context["number_of_likes"], 1)        

    def test_comment_submission(self):
        self.client.post(self.url, {"content": "This is a test comment."})
        self.assertEqual(self.note.comments.count(), 1)


class LikeNoteViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.note = Note.objects.create(
            title="Test Note",
            department="Philosophy",
            subject="Modern Philosophy",
            content="Test content",
            user=self.user,
        )
        self.url = reverse("notes:like_note", args=[self.note.id])
        self.client.login(username="user", password="Str0ng_p@ssword")

    def test_like_adds(self):
        self.client.post(self.url)
        self.assertTrue(self.note.likes.filter(id=self.user.id).exists())

    def test_like_toggles_off(self):
        self.note.likes.add(self.user)
        self.client.post(self.url)
        self.assertFalse(self.note.likes.filter(id=self.user.id).exists())


class NewNoteViewTests(TestCase):

    def setUp(self):
        self.url = reverse("notes:new_note")
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.client.login(username="user", password="Str0ng_p@ssword")
        self.form_data = {
            "title": "Test Note",
            "department": "Philosophy",
            "subject": "Modern Philosophy",
            "content": "This is a test note content.",
            "file": SimpleUploadedFile("testfile.txt", b"File content."),
        }

    def test_unauthenticated_user_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_new_note_view_save(self):
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().user, self.user)
        self.assertRedirects(response, reverse("notes:notes"))


class EditNoteViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.user2 = User.objects.create_user(username="user2", email="user2@uoi.gr", password="Str0ng_p@ssword")
        self.note = Note.objects.create(
            title="Original Title",
            department="Philosophy",
            subject="Modern Philosophy",
            content="Original content.",
            file=SimpleUploadedFile("testfile.txt", b"Original file content."),
            user=self.user,
        )
        self.url = reverse("notes:edit_note", args=[self.note.id])
        self.client.login(username="user", password="Str0ng_p@ssword")

    def test_unauthenticated_user_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_edit_note_view_permission_denied_for_user2(self):
        self.client.logout()
        self.client.login(username="user2", password="Str0ng_p@ssword")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_edit_note_view_success(self):
        data = {
            "title": "Updated Title",
            "department": "Fine Arts",
            "subject": "Printmaking",
            "content": "Updated content.",
            "file": SimpleUploadedFile(
                "updated_test_file.txt", b"Updated file content."
            ),
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("notes:note", args=[self.note.id]))

        self.note.refresh_from_db()
        self.assertEqual(self.note.title, data["title"])
        self.assertEqual(self.note.department, data["department"])
        self.assertEqual(self.note.subject, data["subject"])
        self.assertEqual(self.note.content, data["content"])
        self.assertTrue(self.note.file.name.startswith("uploads/"))
        self.assertEqual(self.note.file.read(), b"Updated file content.")


class DeleteNoteViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.user2 = User.objects.create_user(username="user2", email="user2@uoi.gr", password="Str0ng_p@ssword")
        self.note = Note.objects.create(
            title="Test Note",
            department="Philosophy",
            subject="Modern Philosophy",
            content="Test content.",
            user=self.user,
        )
        self.url = reverse("notes:delete_note", args=[self.note.id])
        self.client.login(username="user", password="Str0ng_p@ssword")

    def test_delete_note_succeeds(self):
        response = self.client.post(self.url)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
        self.assertRedirects(response, reverse("notes:notes"))

    def test_delete_note_non_owner_denied(self):
        self.client.logout()
        self.client.login(username="user2", password="Str0ng_p@ssword")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())

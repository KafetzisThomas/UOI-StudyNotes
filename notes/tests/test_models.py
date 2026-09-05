import shutil
import tempfile
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Note

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class NoteModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.note_data = {
            "title": "Test Note",
            "department": "Philosophy",
            "subject": "Modern Philosophy",
            "content": "This is test content.",
            "file": SimpleUploadedFile("testfile.txt", b"File content."),
            "user": self.user,
        }

    def test_number_of_likes(self):
        note = Note.objects.create(**self.note_data)
        self.assertEqual(note.number_of_likes(), 0)
        note.likes.add(self.user)
        self.assertEqual(note.number_of_likes(), 1)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

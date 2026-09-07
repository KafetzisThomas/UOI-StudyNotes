from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import RegistrationForm, EmailUpdateForm, NewPasswordChangeForm

User = get_user_model()


class RegistrationFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "username": "user",
            "email": "user@uoi.gr",
            "password1": "Str0ng_p@ssword",
            "password2": "Str0ng_p@ssword",
        }

    def test_valid_data(self):
        form = RegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_weak_password_rejected(self):
        data = self.valid_data | {"password1": "password123", "password2": "password123"}
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_email_domain_rejected(self):
        data = self.valid_data | {"email": "user@gmail.com"}
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)


class EmailUpdateFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")

    def test_valid_email(self):
        form = EmailUpdateForm(instance=self.user, data={"email": "new@uoi.gr"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_email_domain_rejected(self):
        form = EmailUpdateForm(instance=self.user, data={"email": "new@gmail.com"})
        self.assertFalse(form.is_valid(), form.errors)


class NewPasswordChangeFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.valid_data = {
            "old_password": "Str0ng_p@ssword",
            "new_password1": "New_Str0ng_p@ssword",
            "new_password2": "New_Str0ng_p@ssword",
        }
        self.invalid_data = {
            "old_password": "Str0ng_p@ssword",
            "new_password1": "password123",
            "new_password2": "password123",
        }

    def test_password_change_strong(self):
        form = NewPasswordChangeForm(user=self.user, data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_password_change_weak(self):
        form = NewPasswordChangeForm(user=self.user, data=self.invalid_data)
        self.assertFalse(form.is_valid(), form.errors)

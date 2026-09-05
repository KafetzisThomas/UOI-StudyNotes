from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "username": "user",
            "email": "user@uoi.gr",
            "password1": "Str0ng_p@ssword",
            "password2": "Str0ng_p@ssword"
        }
        self.url = reverse("users:register")

    def test_register_view_valid(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse("users:login"))


class AccountViewTests(TestCase):

    def setUp(self):
        self.url = reverse("users:account")
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="SecRet_p@ssword")
        self.client.login(username="user", password="SecRet_p@ssword")

    def test_unauthenticated_user_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_update_username_action(self):
        response = self.client.post(self.url, {"action": "update_username", "username": "new_username"})
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "new_username")

    def test_update_email_action(self):
        response = self.client.post(self.url, {"action": "update_email", "email": "new@uoi.gr"})
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new@uoi.gr")


class UpdatePasswordViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.client.login(username="user", password="Str0ng_p@ssword")
        self.form_data = {
            "old_password": "Str0ng_p@ssword", "new_password1": "New_Str0ng_p@ssword", "new_password2": "New_Str0ng_p@ssword"
        }
        self.url = reverse("users:update_password")

    def test_unauthenticated_user_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_update_password_succeeds(self):
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, reverse("users:account"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("New_Str0ng_p@ssword"))


class DeleteAccountViewTests(TestCase):

    def setUp(self):
        self.url = reverse("users:delete_account")
        self.user = User.objects.create_user(username="user", email="user@uoi.gr", password="Str0ng_p@ssword")
        self.client.login(username="user", password="Str0ng_p@ssword")

    def test_delete_account_succeeds(self):
        response = self.client.post(self.url)
        self.assertEqual(User.objects.count(), 0)
        self.assertRedirects(response, reverse("users:register"))

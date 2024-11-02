"""
This module contains test cases for the following views:
* register, account
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch


@patch("turnstile.fields.TurnstileField.validate", return_value=True)
class RegisterViewTests(TestCase):
    """
    Test case for the register view.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.url = reverse("users:register")

    def test_successful_registration(self, mock: MagicMock) -> None:
        """
        Test that a user can register successfully with valid data.
        """
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password1": "SecRet_p@ssword",
            "password2": "SecRet_p@ssword",
            "captcha_verification": "testsecret",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse("users:login"))

    def test_invalid_form_data(self, mock: MagicMock) -> None:
        """
        Test that the form is not valid with incorrect data.
        """
        data = {
            "username": "",
            "email": "invalid_email",
            "password1": "SecRet_p@ssword",
            "password2": "New_SecRet_p@ssword",
            "captcha_verification": "testsecret",
        }
        self.client.post(self.url, data)
        self.assertEqual(User.objects.count(), 0)  # No user should be created


class AccountViewTests(TestCase):
    """
    Test case for the account view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="SecRet_p@ssword",
        )
        self.url = reverse("users:account")
        self.client.login(username="testuser", password="SecRet_p@ssword")

    def test_successful_account_update(self):
        """
        Test updating account credentials with valid form data.
        """
        data = {
            "username": "updated_user",
            "email": "updated_user@example.com",
            "password1": "New_SecRet_p@ssword",
            "password2": "New_SecRet_p@ssword",
        }
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated_user")
        self.assertEqual(self.user.email, "updated_user@example.com")
        self.assertRedirects(response, self.url)

    def test_invalid_form_data(self):
        """
        Test that invalid form submissions do not update user credentials.
        """
        data = {
            "username": "",  # Invalid: username is required
            "email": "invalid_email",
            "password1": "New_SecRet_p@ssword",
            "password2": "SecRet_p@ssword",
        }
        self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, "")
        self.assertNotEqual(self.user.email, "invalid_email")


class DeleteAccountViewTests(TestCase):
    """
    Test case for the delete_account view.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="SecRet_p@ssword",
        )
        self.url = reverse("users:delete_account")
        self.client.login(username="testuser", password="SecRet_p@ssword")

    def test_successful_account_deletion(self):
        """
        Test that a user account is deleted successfully.
        """
        response = self.client.post(self.url)
        self.assertEqual(User.objects.count(), 0)
        self.assertRedirects(response, reverse("users:register"))

    def test_account_not_found_after_deletion(self):
        """
        Test that the account cannot be accessed after deletion.
        """
        self.client.post(self.url)  # Delete the account
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)  # Attempt to access the deleted user

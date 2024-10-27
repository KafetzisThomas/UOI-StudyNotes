"""
This module contains test cases for the following views:
* register
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterViewTests(TestCase):
    """
    Test case for the register view.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.url = reverse("users:register")

    def test_successful_registration(self):
        """
        Test that a user can register successfully with valid data.
        """
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password1": "SecRet_p@ssword",
            "password2": "SecRet_p@ssword",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse("users:login"))

    def test_invalid_form_data(self):
        """
        Test that the form is not valid with incorrect data.
        """
        data = {
            "username": "",
            "email": "invalid_email",
            "password1": "SecRet_p@ssword",
            "password2": "New_SecRet_p@ssword",
        }
        self.client.post(self.url, data)
        self.assertEqual(User.objects.count(), 0)  # No user should be created

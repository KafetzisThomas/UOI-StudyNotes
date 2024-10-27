"""
This module contains test cases for the following classes:
* CustomUserCreationForm (validation & required fields)
"""

from django.test import TestCase
from ..forms import CustomUserCreationForm


class CustomUserCreationFormTests(TestCase):
    """
    Test suite for the CustomUserCreationForm.
    """

    def setUp(self):
        """
        Set up the test environment by defining valid form data.
        """
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "SecRet_p@ssword",
            "password2": "SecRet_p@ssword",
        }

    def test_form_valid_data(self):
        """
        Test that the form is valid with correct data.
        """
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_required_fields(self):
        """
        Test that the form is invalid if required fields are missing.
        """
        # Test missing username
        data = self.valid_data.copy()
        data.pop("username")
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing email
        data = self.valid_data.copy()
        data.pop("email")
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing password
        data = self.valid_data.copy()
        data.pop("password1")
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing condfirmation password
        data = self.valid_data.copy()
        data.pop("password2")
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_form_password_mismatch(self):
        """
        Test that the form is invalid if passwords do not match.
        """
        data = self.valid_data.copy()
        data["password2"] = "Secretpassword"
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

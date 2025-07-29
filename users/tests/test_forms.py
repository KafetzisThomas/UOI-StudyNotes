"""
This module contains test cases for the following classes,
handling validation & required fields:

* CustomUserCreationForm, CustomAuthenticationForm, UpdateUserForm
"""

from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import CustomUserCreationForm, CustomAuthenticationForm, UpdateUserForm


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
            "email": "testuser@uoi.gr",
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

        # Test missing confirmation password
        data = self.valid_data.copy()
        data.pop("password2")
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_form_invalid_email_domain(self):
        """
        Test that the form is invalid if the email domain is not allowed.
        """
        data = self.valid_data.copy()
        data["email"] = "user@invalid.com"
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


class CustomAuthenticationFormTests(TestCase):
    """
    Test suite for the CustomAuthenticationForm.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@uoi.gr",
            password="SecRet_p@ssword",
        )

    def test_form_valid_data(self):
        """
        Test that the form is valid with correct username and password.
        """
        data = {
            "username": "testuser",
            "password": "SecRet_p@ssword",
        }
        form = CustomAuthenticationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_required_fields(self):
        """
        Test that the form is invalid if required fields are missing.
        """
        # Test missing username
        data = {"password": "SecRet_p@ssword"}
        form = CustomAuthenticationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing password
        data = {"username": "testuser"}
        form = CustomAuthenticationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)


class UpdateUserFormTests(TestCase):
    """
    Test suite for the UpdateUserForm.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@uoi.gr",
            password="SecRet_p@ssword",
        )

    def test_form_valid_data(self):
        """
        Test that the form is valid with correct data.
        """
        data = {
            "username": "new_username",
            "email": "new_email@uoi.gr",
            "password1": "New_SecRet_p@ssword",
            "password2": "New_SecRet_p@ssword",
        }
        form = UpdateUserForm(instance=self.user, data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_required_fields(self):
        """
        Test that the form is invalid if required fields are missing.
        """
        # Test missing username
        data = {"username": "", "email": "new_email@uoi.gr"}
        form = UpdateUserForm(instance=self.user, data=data)
        self.assertFalse(form.is_valid(), form.errors)

        # Test missing email
        data = {"username": "new_username", "email": ""}
        form = UpdateUserForm(instance=self.user, data=data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_passwords_not_matching(self):
        """
        Test that the form raises an error if passwords do not match.
        """
        data = {
            "username": "new_username",
            "email": "new_email@uoi.gr",
            "password1": "New_SecRet_p@ssword",
            "password2": "SecRet_p@ssword",
        }
        form = UpdateUserForm(instance=self.user, data=data)
        self.assertFalse(form.is_valid(), form.errors)

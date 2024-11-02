from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from turnstile.fields import TurnstileField


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 1}
        ),
        required=True,
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control bg-dark text-light"}),
        required=True,
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control bg-dark text-light"}),
        required=True,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control bg-dark text-light"}),
        required=True,
    )
    captcha_verification = TurnstileField(theme="dark", size="flexible")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "captcha_verification")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 1}
        ),
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control bg-dark text-light"}),
        required=True,
    )


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.Textarea(
            attrs={"class": "form-control bg-dark text-light", "rows": 1}
        ),
        required=True,
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control bg-dark text-light"}),
        required=True,
    )
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control bg-dark text-light"}),
        required=False,
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control bg-dark text-light"}),
        required=False,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                self.add_error("password1", e)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

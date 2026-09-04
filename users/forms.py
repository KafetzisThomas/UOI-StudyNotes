from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from zxcvbn import zxcvbn


class RegistrationForm(UserCreationForm):
    email = forms.CharField(label="Email Address", required=True)

    class Meta:
        model = User
        fields = ("email", "username")

    def clean_email(self):
        allowed_domains = ["uoi.gr", "gmail.com", "apple.com", "outlook.com"]
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]
        if domain not in allowed_domains:
            raise ValidationError("Email domain is not allowed. Please use a valid email address.")
        return email


class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)


class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        allowed_domains = ["uoi.gr", "gmail.com", "apple.com", "outlook.com"]
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]
        if domain not in allowed_domains:
            raise ValidationError("Email domain is not allowed. Please use a valid email address.")
        return email


class NewPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",
        widget=forms.PasswordInput(attrs={"autofocus": "autofocus", "class": "form-control"})
    )
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")
        if password:
            result = zxcvbn(password)
            if result["score"] < 3:  # 0 – 4 (=5 levels)
                raise forms.ValidationError("Password is too weak. Try adding more characters, numbers or symbols.")

        return password

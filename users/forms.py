from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from zxcvbn import zxcvbn


class RegistrationForm(UserCreationForm):
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

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        allowed_domains = ["uoi.gr", "gmail.com", "apple.com", "outlook.com"]
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]
        if domain not in allowed_domains:
            raise ValidationError("Email domain is not allowed. Please use a valid email address.")
        return email


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


# class UpdateUserForm(forms.ModelForm):
#     username = forms.CharField(
#         label="Username",
#         widget=forms.Textarea(
#             attrs={"class": "form-control bg-dark text-light", "rows": 1}
#         ),
#         required=True,
#     )
#     email = forms.CharField(
#         label="Email Address",
#         widget=forms.EmailInput(attrs={"class": "form-control bg-dark text-light"}),
#         required=True,
#     )
#     password1 = forms.CharField(
#         label="New Password",
#         widget=forms.PasswordInput(attrs={"class": "form-control bg-dark text-light"}),
#         required=False,
#     )
#     password2 = forms.CharField(
#         label="Confirm New Password",
#         widget=forms.PasswordInput(attrs={"class": "form-control bg-dark text-light"}),
#         required=False,
#     )

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")

#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get("password1")
#         password2 = cleaned_data.get("password2")

#         if password1 and password1 != password2:
#             self.add_error("password2", "Passwords do not match.")

#         if password1:
#             try:
#                 validate_password(password1)
#             except ValidationError as e:
#                 self.add_error("password1", e)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password1")
#         if password:
#             user.set_password(password)
#         if commit:
#             user.save()
#         return user

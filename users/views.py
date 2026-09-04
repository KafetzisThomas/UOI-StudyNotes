from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, CustomAuthenticationForm, UsernameUpdateForm, EmailUpdateForm, NewPasswordChangeForm

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})

@login_required
def account(request):
    user = request.user
    username_form = UsernameUpdateForm(instance=user)
    email_form = EmailUpdateForm(instance=user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_username":
            username_form = UsernameUpdateForm(request.POST, instance=user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Username updated successfully.")
                return redirect("users:account")
        elif action == "update_email":
            email_form = EmailUpdateForm(request.POST, instance=user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully.")
                return redirect("users:account")

    context = {"username_form": username_form, "email_form": email_form}
    return render(request, "users/account.html", context)

@login_required
def update_password(request):
    if request.method == "POST":
        form = NewPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("users:account")
    else:
        form = NewPasswordChangeForm(request.user)

    return render(request, "users/update_password.html", {"form": form})

@login_required
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    messages.error(request, "Your account has been deleted along with all associated data.")
    return redirect("users:register")


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

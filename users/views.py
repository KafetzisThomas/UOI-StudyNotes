from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UpdateUserForm
from django.contrib.auth.views import LoginView
from .utils import send_update_account_notification
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages


def register(request):
    """
    Register a new user.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


def account(request):
    if request.method == "POST":
        form = UpdateUserForm(instance=request.user, data=request.POST)
        user = User.objects.get(id=request.user.id)
        if form.is_valid():
            form.save()
            send_update_account_notification(user) if not settings.DEBUG else None
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(
                request, "Your account credentials have been successfully updated."
            )
            return redirect("users:account")
    else:
        form = UpdateUserForm(instance=request.user)

    context = {"form": form}
    return render(request, "users/account.html", context)


@login_required
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    messages.error(
        request, "Your account has been deleted along with all associated data."
    )
    return redirect("users:register")


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

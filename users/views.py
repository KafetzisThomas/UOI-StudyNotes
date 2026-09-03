from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UpdateUserForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})

@login_required
def account(request):
    if request.method == "POST":
        form = UpdateUserForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your account credentials have been successfully updated.")
            return redirect("users:account")
    else:
        form = UpdateUserForm(instance=request.user)

    return render(request, "users/account.html", {"form": form})

@login_required
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    messages.error(request, "Your account has been deleted along with all associated data.")
    return redirect("users:register")


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

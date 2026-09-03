from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path("account/", views.account, name="account"),
    path("account/delete_account/", views.delete_account, name="delete_account"),
    path("logout/", auth_views.LogoutView.as_view(next_page="users:login"), name="logout"),
]

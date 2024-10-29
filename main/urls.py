from django.urls import path
from django.contrib.auth import views as auth

from .views import HomeView, RegistrationView
from .forms import AccessForm

app_name = "main"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    path(
        "login/",
        auth.LoginView.as_view(
            template_name="main/login.html",
            authentication_form=AccessForm,
        ),
        name="login",
    ),
]

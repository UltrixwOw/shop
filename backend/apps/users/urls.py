from django.urls import path
from .views import (
    RegisterView,
    VerifyEmailView,
    LoginView,
    RefreshView,
    LogoutView,
    CheckEmailView,
    MeView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify/<uidb64>/<token>/", VerifyEmailView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("check-email/", CheckEmailView.as_view()),
    path("me/", MeView.as_view(), name="me"),
]
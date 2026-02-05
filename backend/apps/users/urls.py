from django.urls import path
from .views import RegisterView, VerifyEmailView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify/<uidb64>/<token>/', VerifyEmailView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]

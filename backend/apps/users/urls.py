from .views import RegisterView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify/<uidb64>/<token>/', VerifyEmailView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]

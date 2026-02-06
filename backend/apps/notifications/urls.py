from django.urls import path
from .views import UserNotificationSettingsView, PromoEmailView

urlpatterns = [
    path('settings/', UserNotificationSettingsView.as_view()),
    path('promo/', PromoEmailView.as_view()),
]

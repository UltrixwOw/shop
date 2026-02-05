from django.urls import path
from .views import CheckoutView, UserOrdersView

urlpatterns = [
    path('checkout/', CheckoutView.as_view()),
    path('', UserOrdersView.as_view()),
]

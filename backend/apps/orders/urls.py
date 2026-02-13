from django.urls import path
from .views import CheckoutView, UserOrdersView, OrderStatusUpdateView

urlpatterns = [
    path('checkout/', CheckoutView.as_view()),
    path('', UserOrdersView.as_view()),
    path("<int:order_id>/status/", OrderStatusUpdateView.as_view())
]

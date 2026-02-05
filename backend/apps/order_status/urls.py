from django.urls import path
from .views import OrderStatusUpdateView

urlpatterns = [
    path('order/<int:order_id>/status/', OrderStatusUpdateView.as_view()),
]

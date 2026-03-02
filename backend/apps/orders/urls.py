from django.urls import path
from .views import CancelOrderView, OrderByUUIDView, OrderDetailView, CheckoutView, UserOrdersView, OrderStatusUpdateView

urlpatterns = [
    path('checkout/', CheckoutView.as_view()),
    path('', UserOrdersView.as_view()),
    path('<uuid:uuid>/', OrderDetailView.as_view()),  # ← ВАЖНО
    path("<int:order_id>/status/", OrderStatusUpdateView.as_view()),
    path('by-uuid/<uuid:uuid>/', OrderByUUIDView.as_view()),
    path("<uuid:uuid>/cancel/", CancelOrderView.as_view()),
]

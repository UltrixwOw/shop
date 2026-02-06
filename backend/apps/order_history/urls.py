from django.urls import path
from .views import OrderHistoryView, AdminAllOrdersHistoryView

urlpatterns = [
    path('order/<int:order_id>/history/', OrderHistoryView.as_view()),
    path('admin/all-orders/', AdminAllOrdersHistoryView.as_view()),
]

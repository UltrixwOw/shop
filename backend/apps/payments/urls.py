from django.urls import path
from .views import PaymentView, PaymentTransactionListView, PaymentWebhookView

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),  # путь к POST
    path('transactions/', PaymentTransactionListView.as_view(), name='payment-transactions'),  # GET список транзакций
    path("webhook/", PaymentWebhookView.as_view()),
]

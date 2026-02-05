from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', CartView.as_view()),
    path('add/', AddToCartView.as_view()),
    path('remove/', RemoveFromCartView.as_view()),
]

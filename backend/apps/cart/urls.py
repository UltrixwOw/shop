from django.urls import path
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView, CartSyncView

urlpatterns = [
    path('', CartView.as_view()),
    path('add/', AddToCartView.as_view()),
    path("update/<int:item_id>/", UpdateCartItemView.as_view()),
    path("remove/<int:item_id>/", RemoveCartItemView.as_view()),
    path('sync/', CartSyncView.as_view(), name='cart-sync'),
]

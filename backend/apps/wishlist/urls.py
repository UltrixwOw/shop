# apps/wishlist/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Основные эндпоинты избранного
    path('', views.WishlistListCreateView.as_view(), name='wishlist-list'),
    path('<int:product_id>/', views.WishlistDeleteView.as_view(), name='wishlist-delete'),
    
    # Эндпоинты для шаринга
    path('share/', views.WishlistShareView.as_view(), name='wishlist-share'),
    path('public/<uuid:token>/', views.PublicWishlistView.as_view(), name='wishlist-public'),
    path('sync/', views.WishlistSyncView.as_view(), name='wishlist-sync'),
]
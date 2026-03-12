# apps/wishlist/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Wishlist, WishlistShare
from .serializers import WishlistSerializer, WishlistShareSerializer
import uuid


class WishlistListCreateView(APIView):
    """Получение списка избранного и добавление товара"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """GET /api/wishlist/ - список избранного"""
        items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """POST /api/wishlist/ - добавить товар в избранное"""
        product_id = request.data.get('product')
        
        if not product_id:
            return Response(
                {"error": "product field is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Используем get_or_create для избежания IntegrityError
            item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product_id=product_id
            )
            
            if created:
                serializer = WishlistSerializer(item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "Product already in wishlist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except IntegrityError:
            return Response(
                {"error": "Product already in wishlist"},
                status=status.HTTP_400_BAD_REQUEST
            )


class WishlistDeleteView(APIView):
    """Удаление товара из избранного"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        """DELETE /api/wishlist/<product_id>/ - удалить товар"""
        try:
            item = Wishlist.objects.get(
                user=request.user,
                product_id=product_id
            )
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Wishlist.DoesNotExist:
            return Response(
                {"error": "Product not in wishlist"},
                status=status.HTTP_404_NOT_FOUND
            )


class WishlistShareView(APIView):
    """Управление публичными ссылками на избранное"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """GET /api/wishlist/share/ - получить информацию о шаринге"""
        share, created = WishlistShare.objects.get_or_create(user=request.user)
        serializer = WishlistShareSerializer(share)
        return Response(serializer.data)

    def post(self, request):
        """POST /api/wishlist/share/ - создать/обновить публичную ссылку"""
        is_public = request.data.get('is_public', True)
        
        share, created = WishlistShare.objects.get_or_create(
            user=request.user,
            defaults={'is_public': is_public}
        )
        
        if not created:
            share.is_public = is_public
            share.save()
        
        serializer = WishlistShareSerializer(share)
        return Response(serializer.data)


class PublicWishlistView(APIView):
    """Публичный доступ к избранному по токену"""
    permission_classes = [AllowAny]

    def get(self, request, token):
        """GET /api/wishlist/public/<token>/ - получить публичное избранное"""
        try:
            # Пытаемся преобразовать строку в UUID
            try:
                token_uuid = uuid.UUID(str(token))
            except ValueError:
                return Response(
                    {"error": "Invalid token format"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            share = WishlistShare.objects.get(
                token=token_uuid,
                is_public=True
            )
            
            items = Wishlist.objects.filter(user=share.user)
            product_ids = items.values_list('product_id', flat=True)
            
            return Response({
                "user": share.user.email,
                "products": list(product_ids)
            })
            
        except WishlistShare.DoesNotExist:
            return Response(
                {"error": "Public wishlist not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
class WishlistSyncView(APIView):
    """Синхронизация локального избранного с сервером"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST /api/wishlist/sync/
        Body: {"product_ids": [1, 2, 3]}
        
        Синхронизирует локальный список с сервером:
        - Добавляет товары, которых нет на сервере
        - Удаляет товары, которых нет в локальном списке (опционально)
        """
        product_ids = request.data.get('product_ids', [])
        
        if not isinstance(product_ids, list):
            return Response(
                {"error": "product_ids must be a list"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем текущие товары пользователя
        current_items = Wishlist.objects.filter(user=request.user)
        current_product_ids = set(current_items.values_list('product_id', flat=True))
        new_product_ids = set(product_ids)
        
        # Товары для добавления (есть в локальном, нет на сервере)
        to_add = new_product_ids - current_product_ids
        
        # Товары для удаления (есть на сервере, нет в локальном)
        to_remove = current_product_ids - new_product_ids
        
        # Результаты операций
        results = {
            'added': [],
            'removed': [],
            'failed': []
        }
        
        # Добавляем новые товары
        for product_id in to_add:
            try:
                item, created = Wishlist.objects.get_or_create(
                    user=request.user,
                    product_id=product_id
                )
                if created:
                    results['added'].append(product_id)
            except Exception as e:
                results['failed'].append({
                    'product_id': product_id,
                    'action': 'add',
                    'error': str(e)
                })
        
        # Удаляем товары (опционально - можно пропустить этот шаг)
        # Можно сделать параметром запроса: remove_missing=true/false
        if request.data.get('remove_missing', True):
            for product_id in to_remove:
                try:
                    Wishlist.objects.filter(
                        user=request.user,
                        product_id=product_id
                    ).delete()
                    results['removed'].append(product_id)
                except Exception as e:
                    results['failed'].append({
                        'product_id': product_id,
                        'action': 'remove',
                        'error': str(e)
                    })
        
        # Возвращаем обновленный список
        updated_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(updated_items, many=True)
        
        return Response({
            'results': serializer.data,
            'sync_results': results
        }, status=status.HTTP_200_OK)
# apps/wishlist/serializers.py
from rest_framework import serializers
from .models import Wishlist, WishlistShare

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'created_at']
        read_only_fields = ['id', 'created_at']

class WishlistShareSerializer(serializers.ModelSerializer):
    share_url = serializers.SerializerMethodField()
    
    class Meta:
        model = WishlistShare
        fields = ['token', 'is_public', 'created_at', 'share_url']
        read_only_fields = ['token', 'created_at']
    
    def get_share_url(self, obj):
        if obj.is_public:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(f"/api/wishlist/public/{obj.token}/")
        return None
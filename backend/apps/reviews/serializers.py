from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.username", read_only=True)
    is_mine = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()
    
    debug_user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user_name",
            "debug_user_id",
            "rating",
            "comment",
            "likes_count",
            "liked_by_me",
            "is_approved",
            "is_mine",
            "created_at",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by_me(self, obj):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()

        return False
    
    def get_is_mine(self, obj):
        """Проверяет, принадлежит ли отзыв текущему пользователю"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.user_id == request.user.id
        return False
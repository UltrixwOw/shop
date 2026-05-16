from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductImage
)


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "thumbnail",
            "is_main"
        ]

    def get_image(self, obj):
        request = self.context.get("request")

        if obj.image:
            return request.build_absolute_uri(
                obj.image.url
            )

        return None

    def get_thumbnail(self, obj):
        request = self.context.get("request")

        if obj.thumbnail:
            return request.build_absolute_uri(
                obj.thumbnail.url
            )

        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    average_rating = serializers.FloatField(
        read_only=True
    )

    reviews_count = serializers.IntegerField(
        read_only=True
    )

    user_has_review = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
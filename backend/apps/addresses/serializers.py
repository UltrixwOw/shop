from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):

        user = self.context["request"].user

        # Только один default адрес
        if data.get("is_default"):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        # Запрет редактировать чужой адрес
        if self.instance and self.instance.user != user:
            raise serializers.ValidationError("Not your address")

        return data

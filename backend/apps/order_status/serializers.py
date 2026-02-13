from rest_framework import serializers
from apps.order_history.services import OrderHistoryService

class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ])
    note = serializers.CharField(required=False, allow_blank=True)

class OrderStatusService:

    @staticmethod
    def change_status(order, new_status, user=None, note=None):

        old_status = order.status

        if old_status == new_status:
            return order

        order.status = new_status
        order.save()

        # записываем историю через сервис истории
        OrderHistoryService.record_status(
            order=order,
            status=new_status,
            user=user,
            note=note
        )

        return order
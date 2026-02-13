from apps.order_history.services import OrderHistoryService
from apps.notifications.services import NotificationService
from rest_framework.exceptions import ValidationError

class OrderStatusService:

    # допустимые переходы
    ALLOWED_TRANSITIONS = {
        "pending": ["paid", "cancelled"],
        "paid": ["shipped", "cancelled"],
        "shipped": ["completed"],
        "completed": [],
        "cancelled": [],
    }

    @staticmethod
    def change_status(order, new_status, user=None, note=None):

        current_status = order.status

        # если статус тот же
        if current_status == new_status:
            return order

        # проверяем допустимость перехода
        allowed = OrderStatusService.ALLOWED_TRANSITIONS.get(current_status, [])

        if new_status not in allowed:
            raise ValidationError(
                f"Cannot change order status from '{current_status}' to '{new_status}'"
            )

        # меняем статус
        order.status = new_status
        order.save()

        # пишем историю
        OrderHistoryService.record_status(
            order=order,
            status=new_status,
            user=user,
            note=note
        )

        return order
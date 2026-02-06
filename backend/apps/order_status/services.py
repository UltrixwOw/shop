from apps.order_history.services import OrderHistoryService
from apps.notifications.services import NotificationService

class OrderStatusService:
    @staticmethod
    def change_status(order, new_status, user=None, note=None):
        # Можно добавить проверку допустимых переходов статусов
        order.status = new_status
        order.save()

        # Создаём запись истории
        OrderHistoryService.record_status(order, new_status, user=user, note=note)

        # Отправляем email пользователю
        NotificationService.send_order_status_update(order.user, order)
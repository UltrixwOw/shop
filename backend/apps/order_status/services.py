from apps.order_history.services import OrderHistoryService

class OrderStatusService:
    @staticmethod
    def change_status(order, new_status, user=None, note=None):
        # Можно добавить проверку допустимых переходов статусов
        order.status = new_status
        order.save()

        # Создаём запись истории
        OrderHistoryService.record_status(order, new_status, user=user, note=note)
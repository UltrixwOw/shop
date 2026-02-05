from .models import OrderStatusHistory

class OrderStatusService:
    @staticmethod
    def change_status(order, new_status, user=None, note=None):
        # Можно добавить проверку допустимых переходов статусов
        order.status = new_status
        order.save()

        # Создаём запись истории
        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            changed_by=user,
            note=note
        )

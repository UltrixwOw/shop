from .models import OrderHistory

class OrderHistoryService:
    @staticmethod
    def record_status(order, status, user=None, note=None):
        # Создаем запись в истории
        OrderHistory.objects.create(
            order=order,
            status=status,
            changed_by=user,
            note=note
        )

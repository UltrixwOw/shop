from django.core.mail import send_mail
from django.conf import settings


class NotificationService:

    @staticmethod
    def send_email(subject, message, recipient_list):
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list
        )

    @staticmethod
    def send_order_status_update(user, order):

        # Проверяем подписку
        if not user.notifications.order_updates:
            return

        subject = f"Обновление заказа #{order.id}"
        message = f"Статус вашего заказа изменён: {order.status}"

        NotificationService.send_email(subject, message, [user.email])

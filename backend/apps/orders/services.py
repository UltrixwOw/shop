# apps/orders/services.py

from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def broadcast_stock(product):
    """
    Отправляет real-time обновление остатка товара через WebSocket.
    
    Args:
        product: Экземпляр модели Product с обновленным полем stock
        
    Returns:
        None: Если channel_layer недоступен, тихо завершает работу
    """
    channel_layer = get_channel_layer()

    if not channel_layer:
        # Логирование можно добавить, если нужно отслеживать проблемы
        # print(f"Channel layer not available for product {product.id}")
        return

    async_to_sync(channel_layer.group_send)(
        "stock_updates",  # Группа для обновлений остатков
        {
            "type": "stock_update",
            "product_id": product.id,
            "stock": product.stock,
        }
    )


import logging
import traceback
logger = logging.getLogger(__name__)

class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(user, address, cart):

        logger.error("🚀 ORDER SERVICE START")

        try:
            if not cart:
                logger.error("💥 CART IS NONE")
                raise ValidationError("Cart not found")

            cart_items = (
                cart.items
                .select_related("product")
                .select_for_update()
            )

            count = cart_items.count()
            logger.error(f"Cart items count: {count}")

            if count == 0:
                logger.error("💥 CART EMPTY")
                raise ValidationError("Cart is empty")

            total = 0

            # ✅ STOCK CHECK
            for item in cart_items:
                logger.error(f"Checking item: {item.id}")

                if not item.product:
                    logger.error("💥 PRODUCT IS NONE")
                    raise ValidationError("Product missing")

                logger.error(f"Product: {item.product.name}, stock={item.product.stock}, qty={item.quantity}")

                if item.quantity > item.product.stock:
                    logger.error("💥 NOT ENOUGH STOCK")
                    raise ValidationError(
                        f"{item.product.name} нет в нужном количестве"
                    )

            logger.error("✅ STOCK OK")

            # ✅ CREATE ORDER
            try:
                order = Order.objects.create(
                    user=user,
                    address=address,
                    status="pending"
                )
                logger.error(f"✅ ORDER CREATED: {order.id}")
            except Exception as e:
                logger.error(f"💥 ORDER CREATE ERROR: {e}")
                traceback.print_exc()
                raise

            # ✅ LOOP ITEMS
            for item in cart_items:
                try:
                    product = item.product

                    logger.error(f"Updating stock for {product.name}")

                    product.stock -= item.quantity
                    product.save()

                    logger.error("Stock updated")

                    # 🔥 возможно тут падает
                    try:
                        broadcast_stock(product)
                        logger.error("broadcast_stock OK")
                    except Exception as e:
                        logger.error(f"💥 broadcast_stock ERROR: {e}")

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        product_price=product.price,
                        quantity=item.quantity,
                    )

                    logger.error("OrderItem created")

                    total += product.price * item.quantity

                except Exception as e:
                    logger.error(f"💥 ITEM LOOP ERROR: {e}")
                    traceback.print_exc()
                    raise

            # ✅ FINAL SAVE
            try:
                order.total_price = total
                order.save()
                logger.error(f"✅ TOTAL SAVED: {total}")
            except Exception as e:
                logger.error(f"💥 TOTAL SAVE ERROR: {e}")
                raise

            # ✅ CLEAR CART
            try:
                cart_items.delete()
                logger.error("✅ CART CLEARED")
            except Exception as e:
                logger.error(f"💥 CART DELETE ERROR: {e}")

            logger.error("🚀 ORDER SERVICE END OK")

            return order

        except Exception as e:
            logger.error("💥💥💥 ORDER SERVICE CRASH")
            logger.error(str(e))
            traceback.print_exc()
            raise
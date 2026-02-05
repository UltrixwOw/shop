class PayPalService:
    @staticmethod
    def process_payment(order):
        # симуляция успешной оплаты
        return {"success": True, "provider_payment_id": f"PAYPAL-{order.id}"}

class CardService:
    @staticmethod
    def process_payment(order):
        return {"success": True, "provider_payment_id": f"CARD-{order.id}"}

class CryptoService:
    @staticmethod
    def process_payment(order):
        return {"success": True, "provider_payment_id": f"CRYPTO-{order.id}"}

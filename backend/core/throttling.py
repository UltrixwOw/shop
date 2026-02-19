from rest_framework.throttling import UserRateThrottle


class PaymentThrottle(UserRateThrottle):
    scope = "payments"


class LoginThrottle(UserRateThrottle):
    scope = "login"

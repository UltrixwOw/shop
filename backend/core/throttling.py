from rest_framework.throttling import UserRateThrottle


class PaymentThrottle(UserRateThrottle):
    rate = "5/min"


class LoginThrottle(UserRateThrottle):
    rate = "10/min"

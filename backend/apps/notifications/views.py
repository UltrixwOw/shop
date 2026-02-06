from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .services import NotificationService
from apps.users.models import User


from rest_framework.permissions import IsAuthenticated

from .models import NotificationSubscription
from .serializers import NotificationSubscriptionSerializer

class PromoEmailView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        subject = request.data.get("subject")
        message = request.data.get("message")
        recipients = request.data.get("recipients")  # можно список email или "all"

        if recipients == "all":
            recipients_list = User.objects.filter(is_active=True).values_list('email', flat=True)
        else:
            recipients_list = recipients

        NotificationService.send_email(subject, message, recipients_list)
        return Response({"status": "Emails sent"})

class UserNotificationSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = request.user.notifications
        serializer = NotificationSubscriptionSerializer(subscription)
        return Response(serializer.data)

    def patch(self, request):
        subscription = request.user.notifications
        serializer = NotificationSubscriptionSerializer(subscription, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
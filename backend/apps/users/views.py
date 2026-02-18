from django.shortcuts import render

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .tokens import email_verification_token
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)

        current_site = get_current_site(request)
        link = f"http://{current_site.domain}/api/users/verify/{uid}/{token}/"

        send_mail(
            subject="Подтвердите email",
            message=f"Перейдите по ссылке для активации:\n{link}",
            from_email=None,
            recipient_list=[user.email],
        )

        return Response(
            {"message": "Проверьте email для подтверждения"},
            status=status.HTTP_201_CREATED
        )
        

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except Exception:
            return Response({"error": "Неверная ссылка"}, status=400)

        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email подтверждён"})
        else:
            return Response({"error": "Ссылка устарела"}, status=400)

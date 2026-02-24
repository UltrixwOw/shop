from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken

from .tokens import email_verification_token
from .models import User
from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        # 🔁 Пользователь уже существует
        if user:
            if not user.is_verified:
                self._send_verification_email(request, user)
                return Response(
                    {"message": "Verification email resent"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "User already registered"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🆕 Новый пользователь
        user = User.objects.create_user(
            email=email,
            password=password
        )
        user.is_active = False
        user.is_verified = False
        user.save()

        self._send_verification_email(request, user)

        return Response(
            {"message": "Check your email"},
            status=status.HTTP_201_CREATED
        )

    def _send_verification_email(self, request, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)
        current_site = get_current_site(request)

        link = f"http://{current_site.domain}/api/users/verify/{uid}/{token}/"

        send_mail(
            subject="Подтвердите email",
            message=f"Перейдите по ссылке:\n{link}",
            from_email=None,
            recipient_list=[user.email],
        )

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

        return Response({"error": "Ссылка устарела"}, status=400)
    
class CheckEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            return Response({"exists": True})

        return Response({"exists": False}, status=404)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("Email not verified")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            "access": access_token
        })

        # 🔐 Refresh в HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,  # True в production (HTTPS)
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response
    
class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed("No refresh token")

        try:
            refresh = RefreshToken(refresh_token)
            access = str(refresh.access_token)
        except Exception:
            raise AuthenticationFailed("Invalid refresh token")

        return Response({"access": access})
    
class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"})
        response.delete_cookie("refresh_token")
        return response
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "email": user.email,
            "role": getattr(user, "role", "customer"),
            "is_verified": user.is_verified,
        })
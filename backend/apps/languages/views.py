from django.shortcuts import render
from django.conf import settings
from django.utils import translation
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class LanguageView(APIView):
    """Получить текущий язык и список доступных"""
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            'current': translation.get_language(),
            'available': [{'code': code, 'name': str(name)} for code, name in settings.LANGUAGES],
        }
        return Response(data)

    def post(self, request):
        """Установить новый язык"""
        lang_code = request.data.get('language')
        
        if lang_code in [code for code, _ in settings.LANGUAGES]:
            translation.activate(lang_code)
            response = Response({'status': 'ok', 'language': lang_code})
            
            # Сохраняем язык в cookie на 1 год
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, 
                lang_code, 
                max_age=365 * 24 * 60 * 60,
                httponly=False,  # Чтобы фронтенд мог прочитать
                samesite='Lax',
                secure=not settings.DEBUG  # True в production, False в dev
            )
            return response
        
        return Response({'error': 'Language not supported'}, status=400)
    
class LanguageTestView(APIView):
    def get(self, request):
        lang = request.headers.get('Accept-Language', 'en')

        messages = {
            'en': 'Hello',
            'ru': 'Привет',
            'de': 'Hallo'
        }

        return Response({
            "message": messages.get(lang, 'Hello')
        })
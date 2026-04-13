from django.urls import path
from .views import LanguageView, LanguageTestView

urlpatterns = [
    path('', LanguageView.as_view()),  # GET/POST для языка
    path('current/', LanguageView.as_view()),  # альтернативный вариант
    path('test/', LanguageTestView.as_view()),
]
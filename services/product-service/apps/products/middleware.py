import jwt
import requests
from django.http import JsonResponse
from django.conf import settings

class JWTAuthenticationMiddleware:
    """Middleware для проверки JWT токенов от других сервисов"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем токен только для админских операций
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and '/admin/' not in request.path:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                # В реальном приложении здесь была бы проверка токена через user-service
                # Пока что просто пропускаем
                pass

        response = self.get_response(request)
        return response

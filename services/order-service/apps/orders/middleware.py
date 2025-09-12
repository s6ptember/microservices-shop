from django.http import JsonResponse
from .services import UserService

class JWTAuthenticationMiddleware:
    """Middleware для аутентификации через JWT токены"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем health check и admin
        if request.path in ['/health/', '/admin/']:
            return self.get_response(request)

        # Извлекаем токен
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            # Получаем пользователя через user-service
            user_data = UserService.get_user_from_token(token)
            if user_data:
                request.user_id = user_data['id']
                request.user_email = user_data['email']
                request.user_data = user_data
            else:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        response = self.get_response(request)
        return response

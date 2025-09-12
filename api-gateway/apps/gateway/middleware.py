import time
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings

class RateLimitMiddleware:
    """Middleware для ограничения частоты запросов"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем статические файлы и админку
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return self.get_response(request)

        # Получаем IP адрес клиента
        client_ip = self.get_client_ip(request)

        # Создаем ключ для кэша
        cache_key = f"rate_limit:{client_ip}"

        # Получаем текущее количество запросов
        current_requests = cache.get(cache_key, 0)

        # Проверяем лимит
        if current_requests >= settings.RATE_LIMIT_REQUESTS_PER_MINUTE:
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {settings.RATE_LIMIT_REQUESTS_PER_MINUTE} requests per minute allowed'
            }, status=429)

        # Увеличиваем счетчик
        cache.set(cache_key, current_requests + 1, 60)  # 60 секунд

        response = self.get_response(request)

        # Добавляем заголовки с информацией о лимитах
        response['X-RateLimit-Limit'] = str(settings.RATE_LIMIT_REQUESTS_PER_MINUTE)
        response['X-RateLimit-Remaining'] = str(max(0, settings.RATE_LIMIT_REQUESTS_PER_MINUTE - current_requests - 1))

        return response

    def get_client_ip(self, request):
        """Получение IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

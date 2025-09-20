import requests
import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views import View

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class ProxyView(View):
    """Базовый класс для проксирования запросов к микросервисам"""

    def dispatch(self, request, *args, **kwargs):
        # Логируем запрос
        logger.info(f"Gateway request: {request.method} {request.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Body: {request.body.decode('utf-8') if request.body else 'No body'}")

        # Определяем целевой сервис
        service_name = self.get_service_name(request)
        if not service_name:
            logger.error(f"Service not found for path: {request.path}")
            return JsonResponse({'error': 'Service not found'}, status=404)

        # Получаем URL сервиса
        service_url = settings.MICROSERVICES.get(service_name)
        if not service_url:
            logger.error(f"Service {service_name} not configured")
            return JsonResponse({'error': f'Service {service_name} not configured'}, status=500)

        # Формируем целевой URL
        target_path = self.get_target_path(request)
        target_url = f"{service_url}{target_path}"

        logger.info(f"Proxying to: {target_url}")

        # Проксируем запрос
        return self.proxy_request(request, target_url)

    def get_service_name(self, request):
        """Определение сервиса по URL"""
        path = request.path

        if path.startswith('/api/auth/') or path.startswith('/api/users/'):
            return 'user-service'
        elif path.startswith('/api/products/') or path.startswith('/api/categories/'):
            return 'product-service'
        elif path.startswith('/api/cart/'):
            return 'cart-service'
        elif path.startswith('/api/orders/'):
            return 'order-service'

        return None

    def get_target_path(self, request):
        """Формирование пути для целевого сервиса"""
        # Убираем префикс /api если он есть и добавляем обратно для сервиса
        path = request.path
        if path.startswith('/api/'):
            return path  # Оставляем как есть
        return path

    def proxy_request(self, request, target_url):
        """Проксирование HTTP запроса"""
        try:
            # Подготавливаем headers
            headers = {}

            # Копируем важные заголовки
            important_headers = [
                'Authorization', 'Content-Type', 'Accept', 'User-Agent',
                'Accept-Language', 'Accept-Encoding'
            ]

            for header_name in important_headers:
                header_value = request.headers.get(header_name)
                if header_value:
                    headers[header_name] = header_value

            # Логируем заголовки для отладки
            logger.info(f"Forwarding headers: {headers}")

            # Подготавливаем данные
            data = None
            json_data = None

            if request.method in ['POST', 'PUT', 'PATCH']:
                content_type = request.headers.get('Content-Type', '')

                if 'application/json' in content_type:
                    try:
                        if request.body:
                            json_data = json.loads(request.body.decode('utf-8'))
                            logger.info(f"JSON data: {json_data}")
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.error(f"Failed to parse JSON: {e}")
                        data = request.body
                else:
                    data = request.body

            # Добавляем query parameters
            params = dict(request.GET.items())
            if params:
                logger.info(f"Query params: {params}")

            # Выполняем запрос
            response = requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                json=json_data,
                data=data if json_data is None else None,
                params=params,
                timeout=30
            )

            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.text[:200]}...")  # Логируем первые 200 символов

            # Возвращаем ответ
            django_response = HttpResponse(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('content-type', 'application/json')
            )

            # Копируем важные заголовки ответа
            response_headers_to_copy = ['Content-Type', 'Cache-Control', 'ETag']
            for key in response_headers_to_copy:
                if key in response.headers:
                    django_response[key] = response.headers[key]

            return django_response

        except requests.exceptions.Timeout:
            logger.error(f"Timeout when calling {target_url}")
            return JsonResponse({'error': 'Service timeout'}, status=504)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error when calling {target_url}: {e}")
            return JsonResponse({'error': 'Service unavailable'}, status=503)
        except Exception as e:
            logger.error(f"Error proxying request to {target_url}: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

# Создаем экземпляр для всех API запросов
proxy_view = ProxyView.as_view()

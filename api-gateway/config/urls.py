# ===== api-gateway/config/urls.py =====
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'api-gateway',
        'services': {
            'user-service': 'http://localhost:8004',
            'product-service': 'http://localhost:8001',
            'cart-service': 'http://localhost:8002',
            'order-service': 'http://localhost:8003'
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('api/', include('apps.gateway.urls')),
]

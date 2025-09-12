import requests
import redis
import json
import logging
from django.conf import settings
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class EventBus:
    """Сервис для публикации событий"""

    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def publish_event(self, event_type: str, data: Dict[str, Any]):
        """Публикация события"""
        try:
            event_data = {
                'type': event_type,
                'data': data,
                'timestamp': json.dumps({}, default=str)
            }
            self.redis_client.publish('events', json.dumps(event_data, default=str))
            logger.info(f"Published event: {event_type}")
        except Exception as e:
            logger.error(f"Failed to publish event {event_type}: {e}")

event_bus = EventBus()

class CartService:
    """Сервис для взаимодействия с Cart Service"""

    @staticmethod
    def get_user_cart(user_id: int, token: str) -> Optional[Dict[str, Any]]:
        """Получение корзины пользователя"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{settings.CART_SERVICE_URL}/api/cart/",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get cart for user {user_id}: {e}")
            return None

class ProductService:
    """Сервис для взаимодействия с Product Service"""

    @staticmethod
    def reserve_products(items: List[Dict]) -> bool:
        """Резервирование товаров"""
        try:
            for item in items:
                response = requests.post(
                    f"{settings.PRODUCT_SERVICE_URL}/api/products/{item['product_id']}/reserve/",
                    json={'quantity': item['quantity']},
                    timeout=10
                )
                if response.status_code != 200:
                    logger.error(f"Failed to reserve product {item['product_id']}")
                    # В случае ошибки нужно откатить уже зарезервированные товары
                    return False
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to reserve products: {e}")
            return False

    @staticmethod
    def release_products(items: List[Dict]):
        """Освобождение зарезервированных товаров"""
        try:
            for item in items:
                requests.post(
                    f"{settings.PRODUCT_SERVICE_URL}/api/products/{item['product_id']}/release/",
                    json={'quantity': item['quantity']},
                    timeout=10
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to release products: {e}")

class UserService:
    """Сервис для взаимодействия с User Service"""

    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
        """Получение информации о пользователе по токену"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/api/users/profile/",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user from token: {e}")
            return None

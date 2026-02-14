import redis
from django.conf import settings
from django_redis import get_redis_connection

class RedisLock:
    def __init__(self):
        self.redis = get_redis_connection("default")

    def acquire_lock(self, sku, pedido_id, timeout=5):
        key = f"lock:produto:{sku}"
        return self.redis.set(key, pedido_id, nx=True, ex=timeout)

    def release_lock(self, sku):
        key = f"lock:produto:{sku}"
        self.redis.delete(key)

    def is_locked(self, sku):
        key = f"lock:produto:{sku}"
        return self.redis.exists(key)

class RedisIdempotency:
    def __init__(self):
        self.redis = get_redis_connection("default")

    def save_key(self, idempotency_key, pedido_id):
        key = f"idempotency:{idempotency_key}"
        self.redis.set(key, pedido_id)

    def get_pedido_id(self, idempotency_key):
        key = f"idempotency:{idempotency_key}"
        return self.redis.get(key)

import pytest
from django_redis import get_redis_connection

class TestRedisConnection:
    def test_redis_ping(self):
        redis_conn = get_redis_connection("default")
        assert redis_conn.ping() is True

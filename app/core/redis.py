import json
import logging
import time
from typing import Any, Optional
import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger("app.core.redis")


class CacheEngine:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._redis: Optional[aioredis.Redis] = None
        self._memory_cache: dict[str, tuple[float, str]] = {}
        self._is_redis_available = False

    async def initialize(self) -> None:
        try:
            self._redis = aioredis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_timeout=2.0,
                socket_connect_timeout=2.0,
            )
            await self._redis.ping()
            self._is_redis_available = True
            logger.info("Successfully connected to Redis at %s", self.redis_url)
        except Exception as exc:
            self._is_redis_available = False
            logger.warning(
                "Redis unavailable at %s (%s). Falling back to in-memory TTL cache.",
                self.redis_url,
                exc,
            )

    async def ping(self) -> bool:
        if self._redis and self._is_redis_available:
            try:
                await self._redis.ping()
                return True
            except Exception:
                self._is_redis_available = False
                return False
        return False

    async def get(self, key: str) -> Optional[str]:
        if self._redis and self._is_redis_available:
            try:
                return await self._redis.get(key)
            except Exception as exc:
                logger.warning("Redis GET error for key %s: %s. Using memory fallback.", key, exc)
                self._is_redis_available = False

        # Memory cache fallback
        now = time.time()
        if key in self._memory_cache:
            expires_at, value = self._memory_cache[key]
            if expires_at > now:
                return value
            del self._memory_cache[key]
        return None

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        ttl = ttl if ttl is not None else settings.REDIS_CACHE_TTL_SECONDS
        if self._redis and self._is_redis_available:
            try:
                await self._redis.set(key, value, ex=ttl)
                return True
            except Exception as exc:
                logger.warning("Redis SET error for key %s: %s. Using memory fallback.", key, exc)
                self._is_redis_available = False

        # Memory cache fallback
        self._memory_cache[key] = (time.time() + ttl, value)
        return True

    async def delete(self, key: str) -> bool:
        success = True
        if self._redis and self._is_redis_available:
            try:
                await self._redis.delete(key)
            except Exception as exc:
                logger.warning("Redis DELETE error for key %s: %s", key, exc)
                success = False

        if key in self._memory_cache:
            del self._memory_cache[key]
        return success

    async def get_json(self, key: str) -> Optional[Any]:
        data = await self.get(key)
        if data:
            try:
                return json.loads(data)
            except Exception:
                return None
        return None

    async def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        encoded = json.dumps(value)
        return await self.set(key, encoded, ttl=ttl)

    async def close(self) -> None:
        if self._redis:
            if hasattr(self._redis, "aclose"):
                await self._redis.aclose()
            else:
                await self._redis.close()


cache = CacheEngine(settings.REDIS_URL)

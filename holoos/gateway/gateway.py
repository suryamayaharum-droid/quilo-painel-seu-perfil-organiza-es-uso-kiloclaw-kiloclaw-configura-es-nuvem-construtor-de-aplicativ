"""
HoloOS API Gateway
==================
Rate limiting, authentication, caching, and request routing.
"""

from __future__ import annotations

import logging
import time
import hashlib
import uuid
from typing import Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

logger = logging.getLogger(__name__)


class AuthType(Enum):
    NONE = auto()
    API_KEY = auto()
    JWT = auto()
    OAUTH2 = auto()


@dataclass
class RateLimitRule:
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst_size: int = 10


@dataclass
class APIKey:
    key: str
    name: str
    created_at: float
    expires_at: Optional[float] = None
    permissions: list[str] = field(default_factory=list)
    rate_limit: RateLimitRule = field(default_factory=RateLimitRule)


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self) -> None:
        self._buckets: dict[str, dict] = {}
        logger.info("[RateLimiter] Initialized")

    def check(self, client_id: str, rule: RateLimitRule) -> tuple[bool, str]:
        now = time.time()
        
        if client_id not in self._buckets:
            self._buckets[client_id] = {
                "tokens": rule.burst_size,
                "last_refill": now,
                "minute_count": 0,
                "hour_count": 0,
                "minute_reset": now,
                "hour_reset": now,
            }
        
        bucket = self._buckets[client_id]
        
        if now - bucket["minute_reset"] > 60:
            bucket["minute_count"] = 0
            bucket["minute_reset"] = now
        
        if now - bucket["hour_reset"] > 3600:
            bucket["hour_count"] = 0
            bucket["hour_reset"] = now
        
        if bucket["minute_count"] >= rule.requests_per_minute:
            return False, "Rate limit exceeded (per minute)"
        
        if bucket["hour_count"] >= rule.requests_per_hour:
            return False, "Rate limit exceeded (per hour)"
        
        if bucket["tokens"] <= 0:
            return False, "Rate limit exceeded (burst)"
        
        bucket["tokens"] -= 1
        bucket["minute_count"] += 1
        bucket["hour_count"] += 1
        
        return True, "Allowed"

    def get_status(self) -> dict:
        return {"tracked_clients": len(self._buckets)}


class AuthManager:
    """Authentication and authorization manager."""

    def __init__(self) -> None:
        self._api_keys: dict[str, APIKey] = {}
        self._jwt_secrets: dict[str, str] = {}
        logger.info("[AuthManager] Initialized")

    def create_api_key(self, name: str, permissions: list[str] = None, expires_in: int = None) -> APIKey:
        key = f"holoos_{uuid.uuid4().hex}"
        api_key = APIKey(
            key=key,
            name=name,
            created_at=time.time(),
            expires_at=time.time() + expires_in if expires_in else None,
            permissions=permissions or [],
        )
        self._api_keys[key] = api_key
        logger.info(f"[AuthManager] Created API key: {name}")
        return api_key

    def validate_api_key(self, key: str) -> Optional[APIKey]:
        if key not in self._api_keys:
            return None
        
        api_key = self._api_keys[key]
        
        if api_key.expires_at and time.time() > api_key.expires_at:
            del self._api_keys[key]
            return None
        
        return api_key

    def revoke_api_key(self, key: str) -> bool:
        if key in self._api_keys:
            del self._api_keys[key]
            return True
        return False

    def list_api_keys(self) -> list[dict]:
        return [{"name": k.name, "created": k.created_at, "permissions": k.permissions} for k in self._api_keys.values()]


class RequestCache:
    """Simple in-memory request caching."""

    def __init__(self, default_ttl: int = 60) -> None:
        self.default_ttl = default_ttl
        self._cache: dict[str, tuple[Any, float]] = {}
        logger.info("[RequestCache] Initialized")

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        ttl = ttl or self.default_ttl
        self._cache[key] = (value, time.time() + ttl)

    def invalidate(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        self._cache.clear()

    def get_stats(self) -> dict:
        return {"cached_items": len(self._cache)}


class APIGateway:
    """Main API Gateway coordinating all features."""

    def __init__(self) -> None:
        self.rate_limiter = RateLimiter()
        self.auth_manager = AuthManager()
        self.cache = RequestCache()
        
        self._middleware: list[Callable] = []
        self._routes: dict[str, Callable] = {}
        
        logger.info("[APIGateway] Initialized")

    def register_route(self, path: str, handler: Callable, auth: AuthType = AuthType.NONE) -> None:
        self._routes[path] = handler

    def handle_request(
        self,
        path: str,
        method: str,
        headers: dict = None,
        body: Any = None,
    ) -> dict:
        auth_header = headers.get("Authorization", "") if headers else ""
        client_id = self._extract_client_id(auth_header)
        
        allowed, reason = self.rate_limiter.check(client_id, RateLimitRule())
        if not allowed:
            return {"error": reason, "status": 429}
        
        if path not in self._routes:
            return {"error": "Not found", "status": 404}
        
        handler = self._routes[path]
        
        try:
            result = handler(body) if body else handler()
            return {"data": result, "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}

    def _extract_client_id(self, auth_header: str) -> str:
        if auth_header.startswith("Bearer "):
            return hashlib.md5(auth_header[7:].encode()).hexdigest()[:16]
        return "anonymous"

    def get_status(self) -> dict:
        return {
            "rate_limiter": self.rate_limiter.get_status(),
            "cache": self.cache.get_stats(),
            "routes": len(self._routes),
        }


_gateway: Optional[APIGateway] = None


def get_gateway() -> APIGateway:
    global _gateway
    if _gateway is None:
        _gateway = APIGateway()
    return _gateway


__all__ = [
    "AuthType",
    "RateLimitRule",
    "APIKey",
    "RateLimiter",
    "AuthManager",
    "RequestCache",
    "APIGateway",
    "get_gateway",
]
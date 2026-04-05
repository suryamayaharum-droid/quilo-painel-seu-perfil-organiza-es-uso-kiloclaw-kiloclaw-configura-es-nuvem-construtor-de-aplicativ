"""
HoloOS Config Management
========================
Environment configuration and secrets management.
"""

from __future__ import annotations

import logging
import os
import json
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto

logger = logging.getLogger(__name__)


class ConfigSource(Enum):
    ENV = auto()
    FILE = auto()
    SECRET = auto()


@dataclass
class ConfigValue:
    value: Any
    source: ConfigSource
    encrypted: bool = False


class ConfigManager:
    """Environment and configuration management."""

    def __init__(self) -> None:
        self._config: dict[str, ConfigValue] = {}
        self._load_environment()
        logger.info("[ConfigManager] Initialized")

    def _load_environment(self) -> None:
        env_mappings = {
            "HOLOOS_HOST": ("host", "localhost"),
            "HOLOOS_PORT": ("port", 5000),
            "HOLOOS_DEBUG": ("debug", False),
            "HOLOOS_LOG_LEVEL": ("log_level", "INFO"),
            "HOLOOS_DB_HOST": ("database.host", "localhost"),
            "HOLOOS_DB_PORT": ("database.port", 5432),
            "HOLOOS_REDIS_URL": ("cache.url", "redis://localhost:6379"),
        }

        for env_var, (key, default) in env_mappings.items():
            value = os.environ.get(env_var, default)
            self._config[key] = ConfigValue(value=value, source=ConfigSource.ENV)

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._config:
            return self._config[key].value
        return default

    def set(self, key: str, value: Any, source: ConfigSource = ConfigSource.FILE) -> None:
        self._config[key] = ConfigValue(value=value, source=source)

    def get_all(self) -> dict:
        return {k: v.value for k, v in self._config.items()}

    def is_production(self) -> bool:
        return self.get("env", "development") == "production"


_config_manager: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


__all__ = ["ConfigSource", "ConfigValue", "ConfigManager", "get_config"]
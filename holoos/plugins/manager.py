"""
HoloOS Plugin System
=====================
Dynamic plugin loading and management.
"""

from __future__ import annotations

import logging
import importlib.util
import os
from typing import Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum, auto

logger = logging.getLogger(__name__)


class PluginState(Enum):
    LOADED = auto()
    UNLOADED = auto()
    ACTIVE = auto()
    ERROR = auto()


@dataclass
class Plugin:
    id: str
    name: str
    version: str
    description: str
    entry_point: str
    state: PluginState = PluginState.UNLOADED
    metadata: dict = field(default_factory=dict)


class PluginRegistry:
    """Registry for managing plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}
        self._hooks: dict[str, list[Callable]] = {}
        logger.info("[PluginRegistry] Initialized")

    def register(self, plugin: Plugin) -> None:
        self._plugins[plugin.id] = plugin
        logger.info(f"[PluginRegistry] Registered: {plugin.name}")

    def load(self, plugin_id: str) -> bool:
        if plugin_id not in self._plugins:
            return False
        
        plugin = self._plugins[plugin_id]
        plugin.state = PluginState.LOADED
        logger.info(f"[PluginRegistry] Loaded: {plugin.name}")
        return True

    def unload(self, plugin_id: str) -> bool:
        if plugin_id not in self._plugins:
            return False
        
        plugin = self._plugins[plugin_id]
        plugin.state = PluginState.UNLOADED
        return True

    def activate(self, plugin_id: str) -> bool:
        if plugin_id not in self._plugins:
            return False
        
        plugin = self._plugins[plugin_id]
        plugin.state = PluginState.ACTIVE
        return True

    def get(self, plugin_id: str) -> Optional[Plugin]:
        return self._plugins.get(plugin_id)

    def list_plugins(self, state: PluginState = None) -> list[Plugin]:
        plugins = list(self._plugins.values())
        if state:
            plugins = [p for p in plugins if p.state == state]
        return plugins

    def register_hook(self, hook_name: str, callback: Callable) -> None:
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        self._hooks[hook_name].append(callback)

    def trigger_hook(self, hook_name: str, *args, **kwargs) -> list[Any]:
        results = []
        for callback in self._hooks.get(hook_name, []):
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"[PluginRegistry] Hook error: {e}")
        return results


class PluginManager:
    """Main plugin manager."""

    def __init__(self) -> None:
        self.registry = PluginRegistry()
        logger.info("[PluginManager] Initialized")

    def discover_plugins(self, plugin_dir: str) -> list[Plugin]:
        discovered = []
        if os.path.exists(plugin_dir):
            for file in os.listdir(plugin_dir):
                if file.endswith(".py"):
                    name = file[:-3]
                    plugin = Plugin(
                        id=name,
                        name=name.title(),
                        version="1.0.0",
                        description=f"Discovered plugin: {name}",
                        entry_point=file,
                    )
                    discovered.append(plugin)
                    self.registry.register(plugin)
        return discovered


_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


__all__ = ["PluginState", "Plugin", "PluginRegistry", "PluginManager", "get_plugin_manager"]
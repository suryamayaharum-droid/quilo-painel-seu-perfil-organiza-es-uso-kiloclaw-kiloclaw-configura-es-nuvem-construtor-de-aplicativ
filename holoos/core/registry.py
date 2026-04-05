"""
HoloOS Component Registry
=========================
Central registry for all HoloOS components.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class ComponentRegistry:
    """Central registry for HoloOS components."""

    def __init__(self) -> None:
        self._quantizers: dict[str, type] = {}
        self._transpilers: dict[str, type] = {}
        self._agents: dict[str, type] = {}
        self._tools: dict[str, Callable] = {}
        self._hooks: dict[str, list[Callable]] = {
            "pre_quantize": [],
            "post_quantize": [],
            "pre_transpile": [],
            "post_transpile": [],
            "pre_agent": [],
            "post_agent": [],
        }

    def register_quantizer(self, name: str, cls: type) -> None:
        self._quantizers[name] = cls
        logger.debug(f"Registered quantizer: {name}")

    def register_transpiler(self, name: str, cls: type) -> None:
        self._transpilers[name] = cls
        logger.debug(f"Registered transpiler: {name}")

    def register_agent(self, name: str, cls: type) -> None:
        self._agents[name] = cls
        logger.debug(f"Registered agent: {name}")

    def register_tool(self, name: str, func: Callable) -> None:
        self._tools[name] = func
        logger.debug(f"Registered tool: {name}")

    def register_hook(self, event: str, func: Callable) -> None:
        if event in self._hooks:
            self._hooks[event].append(func)

    def get_quantizer(self, name: str) -> Optional[type]:
        return self._quantizers.get(name)

    def get_transpiler(self, name: str) -> Optional[type]:
        return self._transpilers.get(name)

    def get_agent(self, name: str) -> Optional[type]:
        return self._agents.get(name)

    def get_tool(self, name: str) -> Optional[Callable]:
        return self._tools.get(name)

    def list_quantizers(self) -> list[str]:
        return list(self._quantizers.keys())

    def list_transpilers(self) -> list[str]:
        return list(self._transpilers.keys())

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def execute_hooks(self, event: str, *args: Any, **kwargs: Any) -> None:
        for func in self._hooks.get(event, []):
            try:
                func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Hook {event} failed: {e}")


_global_registry = ComponentRegistry()


def get_registry() -> ComponentRegistry:
    return _global_registry


def register_quantizer(name: str) -> Callable[[type], type]:
    def decorator(cls: type) -> type:
        _global_registry.register_quantizer(name, cls)
        return cls
    return decorator


def register_transpiler(name: str) -> Callable[[type], type]:
    def decorator(cls: type) -> type:
        _global_registry.register_transpiler(name, cls)
        return cls
    return decorator


def register_agent(name: str) -> Callable[[type], type]:
    def decorator(cls: type) -> type:
        _global_registry.register_agent(name, cls)
        return cls
    return decorator


def register_tool(name: str) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        _global_registry.register_tool(name, func)
        return func
    return decorator
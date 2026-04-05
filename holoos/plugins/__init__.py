"""
HoloOS Plugins Module
=====================
Plugin system for extensibility.
"""

from .manager import PluginState, Plugin, PluginRegistry, PluginManager, get_plugin_manager

__all__ = ["PluginState", "Plugin", "PluginRegistry", "PluginManager", "get_plugin_manager"]
"""
HoloOS Distributed Module
=========================
Distributed processing and execution.
"""

from .executor import DistributedExecutor, Node

__all__ = ["DistributedExecutor", "Node"]
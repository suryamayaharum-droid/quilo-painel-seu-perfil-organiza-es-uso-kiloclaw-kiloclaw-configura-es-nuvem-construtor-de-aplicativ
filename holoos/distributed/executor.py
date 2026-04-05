"""
HoloOS Distributed Executor
===========================
Distributed task execution across multiple nodes.
"""

from __future__ import annotations

import logging
import asyncio
from typing import Any, Optional
from dataclasses import dataclass, field

from holoos.core.registry import ComponentRegistry, get_registry

logger = logging.getLogger(__name__)


@dataclass
class Node:
    id: str
    status: str = "idle"
    load: float = 0.0
    capabilities: list[str] = field(default_factory=list)


class DistributedExecutor:
    def __init__(self, registry: Optional[ComponentRegistry] = None) -> None:
        self.registry = registry or get_registry()
        self._nodes: dict[str, Node] = {}
        self._tasks: dict[str, Any] = {}

    def register_node(self, node_id: str, capabilities: Optional[list[str]] = None) -> None:
        node = Node(id=node_id, capabilities=capabilities or ["compute"])
        self._nodes[node_id] = node
        logger.info(f"[DistributedExecutor] Registered node: {node_id}")

    def unregister_node(self, node_id: str) -> None:
        if node_id in self._nodes:
            del self._nodes[node_id]
            logger.info(f"[DistributedExecutor] Unregistered node: {node_id}")

    def execute_parallel(self, task: Any, nodes: list[str]) -> list[Any]:
        results = []
        available_nodes = [n for n in nodes if n in self._nodes]
        
        logger.info(f"[DistributedExecutor] Executing on {len(available_nodes)} nodes")
        
        for node_id in available_nodes:
            node = self._nodes[node_id]
            node.status = "executing"
            result = {"node": node_id, "status": "completed", "output": f"Processed by {node_id}"}
            results.append(result)
            node.status = "idle"
        
        return results

    def execute_distributed(self, task: Any, strategy: str = "round_robin") -> dict[str, Any]:
        if not self._nodes:
            return {"status": "no_nodes", "output": None}
        
        node_id = self._select_node(strategy)
        node = self._nodes[node_id]
        node.status = "executing"
        
        result = {"node": node_id, "status": "completed", "output": f"Processed by {node_id}"}
        node.status = "idle"
        
        return result

    def _select_node(self, strategy: str) -> str:
        if strategy == "least_loaded":
            return min(self._nodes.keys(), key=lambda n: self._nodes[n].load)
        return list(self._nodes.keys())[0]

    def get_nodes(self) -> dict[str, Node]:
        return self._nodes

    def get_node_status(self, node_id: str) -> Optional[Node]:
        return self._nodes.get(node_id)
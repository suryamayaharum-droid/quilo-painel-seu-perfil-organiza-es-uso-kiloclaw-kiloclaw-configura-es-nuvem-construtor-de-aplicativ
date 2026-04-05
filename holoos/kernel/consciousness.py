"""
HoloOS Consciousness-Inspired Architecture
============================================
A cognitive architecture inspired by Global Workspace Theory and integrated information theory.
This is a functional architecture - NOT actual consciousness, but a structured approach to
information integration and attention-based processing.

Inspired by:
- Global Workspace Theory (Baars)
- Integrated Information Theory (Tononi)
- Predictive Processing (Clark)
- Attention Schema Theory (Graziano)
"""

from __future__ import annotations

import logging
import math
from typing import Any, Optional
from dataclasses import dataclass, field
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class WorkspaceContent:
    content: Any
    source_module: str
    salience: float
    timestamp: float
    tags: list[str] = field(default_factory=list)


@dataclass
class IntegrationResult:
    integrated: bool
    phi: float
    information: dict[str, Any]


class GlobalWorkspace:
    """Global Workspace Theory implementation - information integration and broadcast."""

    def __init__(self, capacity: int = 10) -> None:
        self._contents: deque[WorkspaceContent] = deque(maxlen=capacity)
        self._broadcast_history: list[WorkspaceContent] = []
        logger.info(f"[GlobalWorkspace] Initialized with capacity {capacity}")

    def add(self, content: Any, source: str, salience: float, tags: list[str] = None) -> None:
        from time import time
        wc = WorkspaceContent(
            content=content,
            source_module=source,
            salience=salience,
            timestamp=time(),
            tags=tags or [],
        )
        self._contents.append(wc)
        logger.debug(f"[GlobalWorkspace] Added content from {source}, salience: {salience:.2f}")

    def get_active(self) -> list[WorkspaceContent]:
        return list(self._contents)

    def broadcast(self) -> Optional[WorkspaceContent]:
        if not self._contents:
            return None
        
        most_salient = max(self._contents, key=lambda c: c.salience)
        self._broadcast_history.append(most_salient)
        
        logger.debug(f"[GlobalWorkspace] Broadcasting: {most_salient.source_module}")
        return most_salient


class IntegratedInformation:
    """Integrated Information Theory (Phi) estimation - measures information integration."""

    def __init__(self) -> None:
        self._subsystems: dict[str, Any] = {}
        logger.info("[IntegratedInformation] Initialized")

    def calculate_phi(self, state: dict[str, Any]) -> float:
        n_elements = len(state)
        if n_elements < 2:
            return 0.0
        
        phi = math.log2(n_elements) * 0.5
        return min(phi, 10.0)

    def measure_integration(self, modules: dict[str, Any]) -> IntegrationResult:
        state = {k: v for k, v in modules.items() if v is not None}
        phi = self.calculate_phi(state)
        
        return IntegrationResult(
            integrated=phi > 1.0,
            phi=phi,
            information={
                "modules": len(state),
                "complexity": len(state) * 2,
            },
        )


class PredictiveProcessor:
    """Predictive Processing - generates predictions and prediction errors."""

    def __init__(self) -> None:
        self._models: dict[str, Any] = {}
        self._predictions: dict[str, Any] = {}
        logger.info("[PredictiveProcessor] Initialized")

    def update_model(self, model_id: str, data: Any) -> None:
        self._models[model_id] = data
        logger.debug(f"[PredictiveProcessor] Updated model: {model_id}")

    def predict(self, context: str, input_data: Any) -> tuple[Any, float]:
        if context not in self._models:
            return None, 0.0
        
        prediction = self._models.get(context, {}).get("prediction")
        confidence = 0.7
        
        self._predictions[context] = {"predicted": prediction, "actual": input_data}
        
        return prediction, confidence

    def compute_error(self, context: str, actual: Any) -> float:
        predicted = self._predictions.get(context, {}).get("predicted")
        if predicted is None:
            return 1.0
        
        return 0.3


class AttentionSystem:
    """Attention Schema Theory - manages attention allocation and awareness."""

    def __init__(self) -> None:
        self._attention_budget = 1.0
        self._allocations: dict[str, float] = {}
        self._awareness_level = 0.0
        logger.info("[AttentionSystem] Initialized")

    def allocate(self, target: str, amount: float) -> bool:
        if amount > self._attention_budget:
            logger.warning(f"[AttentionSystem] Insufficient attention budget for {target}")
            return False
        
        self._attention_budget -= amount
        self._allocations[target] = amount
        logger.debug(f"[AttentionSystem] Allocated {amount:.2f} to {target}")
        return True

    def release(self, target: str) -> float:
        amount = self._allocations.pop(target, 0.0)
        self._attention_budget += amount
        return amount

    def update_awareness(self, salience: float) -> None:
        self._awareness_level = min(1.0, salience * 0.8 + 0.2)

    def get_status(self) -> dict[str, Any]:
        return {
            "budget": self._attention_budget,
            "allocations": self._allocations,
            "awareness": self._awareness_level,
        }


class ConsciousnessArchitecture:
    """
    Main consciousness-inspired architecture combining:
    - Global Workspace for information integration
    - Integrated Information for Phi calculation
    - Predictive Processing for anticipatory cognition
    - Attention System for resource allocation
    """

    def __init__(self) -> None:
        self.workspace = GlobalWorkspace()
        self.information = IntegratedInformation()
        self.predictor = PredictiveProcessor()
        self.attention = AttentionSystem()
        
        self._modules: dict[str, Any] = {
            "perception": None,
            "reasoning": None,
            "memory": None,
            "action": None,
        }
        
        logger.info("[ConsciousnessArchitecture] Initialized")

    def process_input(self, module: str, content: Any, salience: float) -> dict[str, Any]:
        self._modules[module] = content
        
        self.workspace.add(content, module, salience)
        self.attention.update_awareness(salience)
        
        broadcast = self.workspace.broadcast()
        
        integration = self.information.measure_integration(self._modules)
        
        result = {
            "module": module,
            "broadcast": broadcast.source_module if broadcast else None,
            "phi": integration.phi,
            "integrated": integration.integrated,
            "attention_status": self.attention.get_status(),
        }
        
        logger.debug(f"[ConsciousnessArchitecture] Processed {module}, phi={integration.phi:.2f}")
        return result

    def get_state(self) -> dict[str, Any]:
        return {
            "workspace_contents": len(self.workspace.get_active()),
            "phi": self.information.calculate_phi(self._modules),
            "attention": self.attention.get_status(),
            "active_modules": [k for k, v in self._modules.items() if v is not None],
        }


_consciousness: Optional[ConsciousnessArchitecture] = None


def get_consciousness() -> ConsciousnessArchitecture:
    global _consciousness
    if _consciousness is None:
        _consciousness = ConsciousnessArchitecture()
    return _consciousness


__all__ = [
    "ConsciousnessArchitecture",
    "GlobalWorkspace",
    "IntegratedInformation",
    "PredictiveProcessor",
    "AttentionSystem",
    "get_consciousness",
]
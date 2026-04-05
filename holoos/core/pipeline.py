"""
HoloOS Pipeline Coordinator
===========================
Unified pipeline that orchestrates all HoloOS components.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from holoos.core.types import (
    ModelMetadata,
    QuantizationConfig,
    TranspilerConfig,
    AgentConfig,
    Language,
)
from holoos.core.registry import get_registry, ComponentRegistry

logger = logging.getLogger(__name__)


class PipelineCoordinator:
    """
    Central orchestrator for all HoloOS operations.
    Coordinates quantization, transpilation, agent execution, and distributed processing.
    """

    def __init__(self, registry: Optional[ComponentRegistry] = None) -> None:
        self.registry = registry or get_registry()
        self._initialized = False

    def initialize(self) -> None:
        if self._initialized:
            return
        
        logger.info("Initializing HoloOS Pipeline...")
        
        from holoos.quantizer.engine import QuantizerEngine
        from holoos.compiler.transpiler import UniversalTranspiler
        from holoos.agent.engine import AgentEngine
        
        self.quantizer = QuantizerEngine(self.registry)
        self.transpiler = UniversalTranspiler(self.registry)
        self.agent_engine = AgentEngine(self.registry)
        
        self._initialized = True
        logger.info("HoloOS Pipeline initialized successfully")

    def quantize_model(
        self,
        metadata: ModelMetadata,
        config: QuantizationConfig,
    ) -> ModelMetadata:
        if not self._initialized:
            self.initialize()
        
        logger.info(f"Quantizing model: {metadata.name}")
        self.registry.execute_hooks("pre_quantize", metadata, config)
        
        result = self.quantizer.quantize(metadata, config)
        
        self.registry.execute_hooks("post_quantize", result)
        logger.info(f"Quantization complete: {result.quantization_format}")
        return result

    def transpile_code(
        self,
        code: str,
        config: TranspilerConfig,
    ) -> str:
        if not self._initialized:
            self.initialize()
        
        logger.info(f"Transpiling from {config.source_lang.value} to {config.target_lang.value}")
        self.registry.execute_hooks("pre_transpile", code, config)
        
        result = self.transpiler.transpile(code, config)
        
        self.registry.execute_hooks("post_transpile", result)
        logger.info("Transpilation complete")
        return result

    def execute_agent(
        self,
        prompt: str,
        config: AgentConfig,
    ) -> dict[str, Any]:
        if not self._initialized:
            self.initialize()
        
        logger.info(f"Executing agent: {config.name}")
        self.registry.execute_hooks("pre_agent", prompt, config)
        
        result = self.agent_engine.execute(prompt, config)
        
        self.registry.execute_hooks("post_agent", result)
        return result

    def process_distributed(
        self,
        task: Any,
        nodes: list[str],
    ) -> list[Any]:
        if not self._initialized:
            self.initialize()
        
        from holoos.distributed.executor import DistributedExecutor
        
        executor = DistributedExecutor(self.registry)
        return executor.execute_parallel(task, nodes)


_coordinator: Optional[PipelineCoordinator] = None


def get_coordinator() -> PipelineCoordinator:
    global _coordinator
    if _coordinator is None:
        _coordinator = PipelineCoordinator()
    return _coordinator
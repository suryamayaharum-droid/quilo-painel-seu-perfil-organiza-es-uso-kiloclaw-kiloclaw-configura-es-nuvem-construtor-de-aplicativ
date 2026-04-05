"""
HoloOS - Unified AI System
===========================
A multi-format LLM quantization system with multi-language transpiler,
AI agents, and distributed processing capabilities.
"""

from holoos.core.types import (
    QuantizationFormat,
    Language,
    TensorSpec,
    HoloLayer,
    ModelMetadata,
    QuantizationConfig,
    TranspilerConfig,
    AgentConfig,
)

from holoos.core.pipeline import PipelineCoordinator, get_coordinator
from holoos.core.registry import ComponentRegistry, get_registry

from holoos.quantizer import QuantizerEngine
from holoos.compiler import UniversalTranspiler
from holoos.agent import AgentEngine
from holoos.distributed import DistributedExecutor

__version__ = "0.1.0"

__all__ = [
    "QuantizationFormat",
    "Language",
    "TensorSpec",
    "HoloLayer",
    "ModelMetadata",
    "QuantizationConfig",
    "TranspilerConfig",
    "AgentConfig",
    "PipelineCoordinator",
    "get_coordinator",
    "ComponentRegistry",
    "get_registry",
    "QuantizerEngine",
    "UniversalTranspiler",
    "AgentEngine",
    "DistributedExecutor",
]
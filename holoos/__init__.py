"""
HoloOS - Unified AI System
===========================
A multi-format LLM quantization system with multi-language transpiler,
AI agents, distributed processing, ethical core, self-modeling kernel,
and autonomous code generation capabilities.
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
from holoos.core.ethical import EthicalCore, get_ethical_core, evaluate_action

from holoos.quantizer import QuantizerEngine
from holoos.compiler import UniversalTranspiler
from holoos.agent import AgentEngine
from holoos.distributed import DistributedExecutor
from holoos.kernel import (
    SelfAttentionKernel,
    get_self_kernel,
    ConsciousnessArchitecture,
    get_consciousness,
)
from holoos.generator import AutonomousCodeGenerator, get_code_generator

__version__ = "0.2.0"

__all__ = [
    # Core types
    "QuantizationFormat",
    "Language",
    "TensorSpec",
    "HoloLayer",
    "ModelMetadata",
    "QuantizationConfig",
    "TranspilerConfig",
    "AgentConfig",
    
    # Pipeline
    "PipelineCoordinator",
    "get_coordinator",
    
    # Registry
    "ComponentRegistry",
    "get_registry",
    
    # Ethical Core
    "EthicalCore",
    "get_ethical_core",
    "evaluate_action",
    
    # Modules
    "QuantizerEngine",
    "UniversalTranspiler",
    "AgentEngine",
    "DistributedExecutor",
    
    # Kernel
    "SelfAttentionKernel",
    "get_self_kernel",
    "ConsciousnessArchitecture",
    "get_consciousness",
    
    # Generator
    "AutonomousCodeGenerator",
    "get_code_generator",
]
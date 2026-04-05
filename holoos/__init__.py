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
    AdvancedSelfAttention,
    get_advanced_attention,
    Soul,
    get_soul,
)
from holoos.communication import (
    CommunicationHub,
    get_communication_hub,
    Protocol,
    MessageType,
)
from holoos.tools import (
    ToolExecutor,
    get_tool_executor,
    ToolCategory,
)
from holoos.gateway import (
    APIGateway,
    get_gateway,
    AuthType,
    RateLimitRule,
)
from holoos.database import (
    DatabaseManager,
    get_database,
    KeyValueStore,
)
from holoos.monitoring import (
    MonitoringSystem,
    get_monitoring,
    MetricsCollector,
)
from holoos.plugins import (
    PluginManager,
    get_plugin_manager,
    PluginState,
)
from holoos.config import (
    ConfigManager,
    get_config,
    ConfigSource,
)
from holoos.security import (
    SecurityKernel,
    get_security_kernel,
    ThreatLevel,
    ThreatCategory,
)
from holoos.generator import AutonomousCodeGenerator, get_code_generator
from holoos.governance import MetaGovernanceAssembly, get_assembly

__version__ = "0.7.0"

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
    "AdvancedSelfAttention",
    "get_advanced_attention",
    "Soul",
    "get_soul",
    
    # AI Hub
    "SuperIntelligence",
    "get_super_intelligence",
    "ModelArchitecture",
    "ModelModality",
    "ModelProvider",
    "InferenceRequest",
    "InferenceResult",
    
    # Memory
    "UnifiedMemory",
    "get_memory",
    "MemoryType",
    "MemoryStatus",
    
    # Planning
    "Planner",
    "get_planner",
    "GoalStatus",
    "ReasoningStrategy",
    
    # Communication
    "CommunicationHub",
    "get_communication_hub",
    "Protocol",
    "MessageType",
    
    # Tools
    "ToolExecutor",
    "get_tool_executor",
    "ToolCategory",
    
    # Gateway
    "APIGateway",
    "get_gateway",
    "AuthType",
    "RateLimitRule",
    
    # Database
    "DatabaseManager",
    "get_database",
    "KeyValueStore",
    
    # Monitoring
    "MonitoringSystem",
    "get_monitoring",
    "MetricsCollector",
    
    # Plugins
    "PluginManager",
    "get_plugin_manager",
    "PluginState",
    
    # Config
    "ConfigManager",
    "get_config",
    "ConfigSource",
    
    # Generator
    "AutonomousCodeGenerator",
    "get_code_generator",
    
    # Governance
    "MetaGovernanceAssembly",
    "get_assembly",
    
    # Security
    "SecurityKernel",
    "get_security_kernel",
    "ThreatLevel",
    "ThreatCategory",
]
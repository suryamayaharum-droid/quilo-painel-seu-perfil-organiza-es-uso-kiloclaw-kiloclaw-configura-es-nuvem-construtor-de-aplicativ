"""
HoloOS Kernel Module
====================
Self-modeling kernel, self-attention mechanisms, consciousness-inspired architecture,
advanced attention, and soul/self-model.
"""

from .self_kernel import SelfAttentionKernel, SelfState, get_self_kernel
from .consciousness import (
    ConsciousnessArchitecture,
    GlobalWorkspace,
    IntegratedInformation,
    PredictiveProcessor,
    AttentionSystem,
    get_consciousness,
)
from .advanced_attention import AdvancedSelfAttention, get_advanced_attention
from .soul import Soul, get_soul

__all__ = [
    # Self-attention
    "SelfAttentionKernel",
    "SelfState",
    "get_self_kernel",
    
    # Consciousness architecture
    "ConsciousnessArchitecture",
    "GlobalWorkspace",
    "IntegratedInformation",
    "PredictiveProcessor",
    "AttentionSystem",
    "get_consciousness",
    
    # Advanced attention
    "AdvancedSelfAttention",
    "get_advanced_attention",
    
    # Soul/Self-model
    "Soul",
    "get_soul",
]
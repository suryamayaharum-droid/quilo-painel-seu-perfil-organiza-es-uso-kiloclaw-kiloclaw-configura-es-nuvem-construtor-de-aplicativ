"""
HoloOS AI Module
================
AI integration hub with models, inference, and orchestration.
"""

from .hub import (
    ModelArchitecture,
    ModelModality,
    ModelProvider,
    ModelSpec,
    InferenceRequest,
    InferenceResult,
    ModelRegistry,
    InferenceEngine,
    ModelOrchestrator,
    SuperIntelligence,
    get_super_intelligence,
)

__all__ = [
    "ModelArchitecture",
    "ModelModality",
    "ModelProvider",
    "ModelSpec",
    "InferenceRequest",
    "InferenceResult",
    "ModelRegistry",
    "InferenceEngine",
    "ModelOrchestrator",
    "SuperIntelligence",
    "get_super_intelligence",
]
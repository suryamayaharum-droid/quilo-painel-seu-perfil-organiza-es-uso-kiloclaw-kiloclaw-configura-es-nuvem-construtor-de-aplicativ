"""
HoloOS Security Module
========================
Self-defense, threat detection, intrusion prevention, and security policies.
"""

from .kernel import (
    SecurityKernel,
    ThreatDetector,
    IntrusionPreventionSystem,
    SecurityPolicyEngine,
    EncryptionModule,
    AuditLogger,
    ThreatLevel,
    ThreatCategory,
    get_security_kernel,
)

__all__ = [
    "SecurityKernel",
    "ThreatDetector",
    "IntrusionPreventionSystem",
    "SecurityPolicyEngine",
    "EncryptionModule",
    "AuditLogger",
    "ThreatLevel",
    "ThreatCategory",
    "get_security_kernel",
]
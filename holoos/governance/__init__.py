"""
HoloOS Governance Module
========================
Meta-governance assembly and hierarchical agent coordination.
"""

from .assembly import (
    MetaGovernanceAssembly,
    GovernanceChamber,
    ExecutiveBranch,
    JudiciaryBranch,
    AssemblyMember,
    AgentRole,
    get_assembly,
)

__all__ = [
    "MetaGovernanceAssembly",
    "GovernanceChamber",
    "ExecutiveBranch",
    "JudiciaryBranch",
    "AssemblyMember",
    "AgentRole",
    "get_assembly",
]
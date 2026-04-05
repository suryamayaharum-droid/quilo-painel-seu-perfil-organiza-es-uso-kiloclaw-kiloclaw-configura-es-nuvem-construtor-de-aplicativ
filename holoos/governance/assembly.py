"""
HoloOS Meta-Governance Assembly
===============================
Hierarchical multi-agent governance system with assembly of specialized intelligences.
Inspired by democratic governance, swarm intelligence, and cognitive architectures.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    WORKER = auto()
    COORDINATOR = auto()
    LEGISLATOR = auto()
    JUDICIARY = auto()
    EXECUTIVE = auto()
    OBSERVER = auto()


class VoteType(Enum):
    PROPOSE = auto()
    APPROVE = auto()
    REJECT = auto()
    AMEND = auto()
    VETO = auto()


@dataclass
class Vote:
    agent_id: str
    vote_type: VoteType
    proposal_id: str
    stance: bool
    reasoning: str
    timestamp: float


@dataclass
class Proposal:
    id: str
    title: str
    description: str
    proposer: str
    votes: list[Vote] = field(default_factory=list)
    status: str = "pending"
    created_at: float = field(default_factory=time.time)


@dataclass
class AgentIdentity:
    id: str
    name: str
    role: AgentRole
    specialization: str
    authority_level: int
    capabilities: list[str] = field(default_factory=list)


class AssemblyMember:
    def __init__(
        self,
        agent_id: str,
        name: str,
        role: AgentRole,
        specialization: str,
        authority_level: int = 1,
    ) -> None:
        self.identity = AgentIdentity(
            id=agent_id,
            name=name,
            role=role,
            specialization=specialization,
            authority_level=authority_level,
        )
        self._proposals_voted: set[str] = set()
        self._performance_score = 1.0
        self._resource_allocation = 0.0
        logger.info(f"[AssemblyMember] Initialized {name} as {role.name}")

    def vote(self, proposal: Proposal, stance: bool, reasoning: str) -> Vote:
        vote = Vote(
            agent_id=self.identity.id,
            vote_type=VoteType.PROPOSE if stance else VoteType.REJECT,
            proposal_id=proposal.id,
            stance=stance,
            reasoning=reasoning,
            timestamp=time.time(),
        )
        self._proposals_voted.add(proposal.id)
        return vote

    def can_vote_on(self, proposal: Proposal) -> bool:
        return proposal.id not in self._proposals_voted

    def update_performance(self, score: float) -> None:
        self._performance_score = (self._performance_score + score) / 2

    def get_status(self) -> dict[str, Any]:
        return {
            "id": self.identity.id,
            "name": self.identity.name,
            "role": self.identity.role.name,
            "authority": self.identity.authority_level,
            "performance": self._performance_score,
            "votes_cast": len(self._proposals_voted),
        }


class GovernanceChamber:
    """Legislative chamber for proposing and voting on system policies."""

    def __init__(self, name: str, required_approval: float = 0.5) -> None:
        self.name = name
        self.members: list[AssemblyMember] = []
        self.proposals: list[Proposal] = []
        self.required_approval = required_approval
        logger.info(f"[GovernanceChamber] {name} initialized")

    def add_member(self, member: AssemblyMember) -> None:
        self.members.append(member)
        logger.info(f"[GovernanceChamber] Added {member.identity.name}")

    def submit_proposal(self, title: str, description: str, proposer: str) -> Proposal:
        proposal = Proposal(
            id=f"prop_{len(self.proposals)}_{int(time.time())}",
            title=title,
            description=description,
            proposer=proposer,
        )
        self.proposals.append(proposal)
        logger.info(f"[GovernanceChamber] Proposal submitted: {title}")
        return proposal

    def vote_on_proposal(self, proposal_id: str, member: AssemblyMember, stance: bool, reasoning: str) -> bool:
        proposal = next((p for p in self.proposals if p.id == proposal_id), None)
        if not proposal or not member.can_vote_on(proposal):
            return False
        
        vote = member.vote(proposal, stance, reasoning)
        proposal.votes.append(vote)
        
        if len(proposal.votes) >= len(self.members) * 0.3:
            approval = sum(1 for v in proposal.votes if v.stance) / len(proposal.votes)
            if approval >= self.required_approval:
                proposal.status = "approved"
            elif approval < 1 - self.required_approval:
                proposal.status = "rejected"
        
        return True

    def get_active_proposals(self) -> list[Proposal]:
        return [p for p in self.proposals if p.status == "pending"]


class ExecutiveBranch:
    """Executive branch for executing approved policies."""

    def __init__(self) -> None:
        self._policies: dict[str, Any] = {}
        self._action_queue: deque = deque(maxlen=100)
        logger.info("[ExecutiveBranch] Initialized")

    def execute_policy(self, policy: dict[str, Any]) -> dict[str, Any]:
        result = {
            "policy_id": policy.get("id"),
            "executed": True,
            "timestamp": time.time(),
            "outcome": "success",
        }
        self._policies[policy.get("id", "")] = policy
        logger.info(f"[ExecutiveBranch] Executed: {policy.get('title', 'unknown')}")
        return result

    def queue_action(self, action: dict[str, Any]) -> None:
        self._action_queue.append(action)

    def get_active_policies(self) -> dict[str, Any]:
        return self._policies


class JudiciaryBranch:
    """Judiciary for interpreting rules and resolving disputes."""

    def __init__(self) -> None:
        self._precedents: list[dict[str, Any]] = []
        logger.info("[JudiciaryBranch] Initialized")

    def review_action(self, action: dict[str, Any]) -> tuple[bool, str]:
        harmful_patterns = ["harm", "malware", "exploit", "unauthorized"]
        action_str = str(action).lower()
        
        for pattern in harmful_patterns:
            if pattern in action_str:
                return False, f"Blocked: contains harmful pattern '{pattern}'"
        
        return True, "Action approved"

    def add_precedent(self, case: dict[str, Any]) -> None:
        self._precedents.append(case)

    def get_precedents(self) -> list[dict[str, Any]]:
        return self._precedents


class MetaGovernanceAssembly:
    """
    Multi-tier governance system with specialized chambers.
    
    Structure:
    - Assembly: Overall governance body
    - Legislative: Proposes and votes on policies
    - Executive: Executes approved policies
    - Judiciary: Reviews and interprets rules
    """

    def __init__(self) -> None:
        self.legislative = GovernanceChamber("General Assembly", required_approval=0.6)
        self.executive = ExecutiveBranch()
        self.judiciary = JudiciaryBranch()
        
        self._coordination_layer: dict[str, Any] = {}
        self._resource_pool: float = 1.0
        
        self._initialize_default_agents()
        
        logger.info("[MetaGovernanceAssembly] Initialized")

    def _initialize_default_agents(self) -> None:
        self.legislative.add_member(AssemblyMember(
            agent_id="coordinator_1",
            name="System Coordinator",
            role=AgentRole.COORDINATOR,
            specialization="resource_allocation",
            authority_level=3,
        ))
        
        self.legislative.add_member(AssemblyMember(
            agent_id="worker_1",
            name="Code Worker",
            role=AgentRole.WORKER,
            specialization="code_generation",
            authority_level=1,
        ))
        
        self.legislative.add_member(AssemblyMember(
            agent_id="worker_2",
            name="Analysis Worker",
            role=AgentRole.WORKER,
            specialization="analysis",
            authority_level=1,
        ))
        
        self.legislative.add_member(AssemblyMember(
            agent_id="observer_1",
            name="System Observer",
            role=AgentRole.OBSERVER,
            specialization="monitoring",
            authority_level=1,
        ))

    def propose_policy(self, title: str, description: str, proposer: str) -> Proposal:
        return self.legislative.submit_proposal(title, description, proposer)

    def vote_on_policy(self, proposal_id: str, member_id: str, stance: bool, reasoning: str) -> bool:
        member = next((m for m in self.legislative.members if m.identity.id == member_id), None)
        if not member:
            return False
        return self.legislative.vote_on_proposal(proposal_id, member, stance, reasoning)

    def execute_approved_action(self, action: dict[str, Any]) -> dict[str, Any]:
        approved, reason = self.judiciary.review_action(action)
        
        if not approved:
            return {"status": "blocked", "reason": reason}
        
        return self.executive.execute_policy(action)

    def get_assembly_status(self) -> dict[str, Any]:
        return {
            "members": [m.get_status() for m in self.legislative.members],
            "pending_proposals": len(self.legislative.get_active_proposals()),
            "active_policies": len(self.executive.get_active_policies()),
            "precedents": len(self.judiciary.get_precedents()),
            "resource_pool": self._resource_pool,
        }

    def add_agent(self, agent_id: str, name: str, role: AgentRole, specialization: str, authority: int = 1) -> None:
        member = AssemblyMember(agent_id, name, role, specialization, authority)
        self.legislative.add_member(member)


_assembly: Optional[MetaGovernanceAssembly] = None


def get_assembly() -> MetaGovernanceAssembly:
    global _assembly
    if _assembly is None:
        _assembly = MetaGovernanceAssembly()
    return _assembly


__all__ = [
    "MetaGovernanceAssembly",
    "GovernanceChamber",
    "ExecutiveBranch",
    "JudiciaryBranch",
    "AssemblyMember",
    "AgentRole",
    "Vote",
    "Proposal",
    "get_assembly",
]
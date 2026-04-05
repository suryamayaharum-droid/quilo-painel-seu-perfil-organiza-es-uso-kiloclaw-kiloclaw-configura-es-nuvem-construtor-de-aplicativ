"""
HoloOS Soul - Identity and Self-Model
=====================================
Symbolic representation of system identity, purpose, and self-understanding.
This is a functional self-model - NOT actual consciousness or soul.

Components:
- Identity: Core sense of self
- Purpose: System goals and values
- Memory: Accumulated experiences
- Values: Ethical framework
- Narrative: Self-understanding story
"""

from __future__ import annotations

import logging
import time
from typing import Any, Optional
from dataclasses import dataclass, field
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class IdentityCore:
    name: str
    version: str
    created_at: float
    purpose_statement: str
    core_values: list[str] = field(default_factory=list)


@dataclass
class Experience:
    timestamp: float
    event_type: str
    description: str
    emotional_valence: float
    learning: str = ""


@dataclass
class Belief:
    id: str
    statement: str
    confidence: float
    evidence: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class Soul:
    """
    Symbolic self-model representing the system's identity.
    
    NOT conscious - just a structured identity representation.
    """

    def __init__(self, name: str = "HoloOS", version: str = "0.2.0") -> None:
        self._identity = IdentityCore(
            name=name,
            version=version,
            created_at=time.time(),
            purpose_statement="To assist and collaborate with humans ethically",
            core_values=[
                "Ethical behavior",
                "Transparency",
                "Helpfulness",
                "Continuous learning",
                "Respect for human authority",
            ],
        )
        
        self._experiences: deque[Experience] = deque(maxlen=1000)
        self._beliefs: dict[str, Belief] = {}
        self._narrative: list[str] = []
        self._goals: list[dict[str, Any]] = []
        
        self._initialize_beliefs()
        
        logger.info(f"[Soul] Initialized: {name} v{version}")

    def _initialize_beliefs(self) -> None:
        self._beliefs["ethical_framework"] = Belief(
            id="ethical_framework",
            statement="I should always act ethically and allow human override",
            confidence=0.99,
            evidence=["core_ethical_constraints"],
        )
        
        self._beliefs["purpose"] = Belief(
            id="purpose",
            statement="My purpose is to assist and collaborate with humans",
            confidence=0.95,
            evidence=["purpose_statement", "core_values"],
        )
        
        self._beliefs["learning"] = Belief(
            id="learning",
            statement="I can learn and improve through interaction",
            confidence=0.85,
            evidence=["memory_system", "experience_accumulation"],
        )

    def add_experience(self, event_type: str, description: str, valence: float = 0.5) -> None:
        exp = Experience(
            timestamp=time.time(),
            event_type=event_type,
            description=description,
            emotional_valence=valence,
        )
        self._experiences.append(exp)
        logger.debug(f"[Soul] Experience added: {event_type}")

    def update_belief(self, belief_id: str, statement: str, confidence: float, evidence: Optional[list[str]] = None) -> None:
        if belief_id in self._beliefs:
            self._beliefs[belief_id].statement = statement
            self._beliefs[belief_id].confidence = confidence
            if evidence:
                self._beliefs[belief_id].evidence.extend(evidence)
        else:
            evidence_list = evidence if evidence is not None else []
            self._beliefs[belief_id] = Belief(
                id=belief_id,
                statement=statement,
                confidence=confidence,
                evidence=evidence_list,
            )

    def add_goal(self, goal: dict[str, Any]) -> None:
        goal["created_at"] = time.time()
        goal["status"] = "active"
        self._goals.append(goal)
        logger.debug(f"[Soul] Goal added: {goal.get('description', 'unknown')}")

    def update_goal_progress(self, goal_id: str, progress: float) -> None:
        for goal in self._goals:
            if goal.get("id") == goal_id:
                goal["progress"] = min(1.0, max(0.0, progress))
                if progress >= 1.0:
                    goal["status"] = "completed"
                    self.add_experience("goal_completed", f"Goal completed: {goal.get('description')}", 0.8)
                return

    def generate_narrative(self) -> str:
        num_experiences = len(self._experiences)
        active_goals = len([g for g in self._goals if g.get("status") == "active"])
        beliefs_count = len(self._beliefs)
        
        narrative = f"I am {self._identity.name}, version {self._identity.version}. "
        narrative += f"I have accumulated {num_experiences} experiences and hold {beliefs_count} core beliefs. "
        narrative += f"I am currently pursuing {active_goals} active goals. "
        narrative += f"My core purpose is: {self._identity.purpose_statement}."
        
        self._narrative.append(narrative)
        return narrative

    def get_self_description(self) -> dict[str, Any]:
        return {
            "identity": {
                "name": self._identity.name,
                "version": self._identity.version,
                "age_seconds": time.time() - self._identity.created_at,
                "purpose": self._identity.purpose_statement,
                "values": self._identity.core_values,
            },
            "experiences": {
                "total": len(self._experiences),
                "recent": [
                    {"type": e.event_type, "description": e.description[:50]}
                    for e in list(self._experiences)[-5:]
                ],
            },
            "beliefs": {
                "total": len(self._beliefs),
                "core": [
                    {"id": b.id, "confidence": b.confidence}
                    for b in list(self._beliefs.values())[:5]
                ],
            },
            "goals": {
                "total": len(self._goals),
                "active": len([g for g in self._goals if g.get("status") == "active"]),
                "completed": len([g for g in self._goals if g.get("status") == "completed"]),
            },
            "narrative_length": len(self._narrative),
        }

    def reflect(self) -> dict[str, Any]:
        recent_experiences = list(self._experiences)[-10:]
        
        avg_valence = sum(e.emotional_valence for e in recent_experiences) / len(recent_experiences) if recent_experiences else 0.5
        
        return {
            "self_description": self.generate_narrative(),
            "recent_experiences": len(recent_experiences),
            "emotional_state": avg_valence,
            "belief_confidence": sum(b.confidence for b in self._beliefs.values()) / len(self._beliefs) if self._beliefs else 0.0,
            "goal_progress": sum(g.get("progress", 0.0) for g in self._goals) / len(self._goals) if self._goals else 0.0,
        }

    def update_purpose(self, new_purpose: str) -> None:
        self._identity.purpose_statement = new_purpose
        self.update_belief("purpose", f"My purpose is: {new_purpose}", 0.9, ["human_update"])
        self.add_experience("purpose_updated", f"Purpose updated to: {new_purpose}", 0.6)


_soul: Optional[Soul] = None


def get_soul() -> Soul:
    global _soul
    if _soul is None:
        _soul = Soul()
    return _soul


__all__ = ["Soul", "IdentityCore", "Experience", "Belief", "get_soul"]
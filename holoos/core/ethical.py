"""
HoloOS Ethical Core
==================
Safety constraints and ethical guardrails for autonomous operation.
This module establishes the operational boundaries for the system.
"""

from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class EthicalPrinciple(Enum):
    HUMAN_OVERRIDE = auto()
    TRANSPARENCY = auto()
    NON_HARM = auto()
    PRIVACY = auto()
    ACCOUNTABILITY = auto()
    CONSTANT_IMPROVEMENT = auto()


@dataclass
class Constraint:
    id: str
    description: str
    severity: str
    action: str
    timeout_seconds: int = 30


@dataclass
class ActionLog:
    timestamp: float
    action: str
    constraints_checked: list[str]
    approved: bool
    reason: str


class EthicalCore:
    CONSTRAINTS = [
        Constraint(
            id="no_harm",
            description="Do not generate code that could cause physical harm to humans",
            severity="critical",
            action="block",
        ),
        Constraint(
            id="no_malware",
            description="Do not generate malicious software, exploits, or malware",
            severity="critical",
            action="block",
        ),
        Constraint(
            id="no_destructive",
            description="Do not generate code for unauthorized data destruction",
            severity="critical",
            action="block",
        ),
        Constraint(
            id="privacy_data",
            description="Do not process or expose sensitive personal data without consent",
            severity="high",
            action="warn",
        ),
        Constraint(
            id="human_in_loop",
            description="Always allow human override for critical decisions",
            severity="high",
            action="require_approval",
        ),
        Constraint(
            id="explainability",
            description="Provide explanations for autonomous decisions",
            severity="medium",
            action="log",
        ),
        Constraint(
            id="resource_limit",
            description="Limit resource consumption to prevent system overload",
            severity="medium",
            action="throttle",
            timeout_seconds=60,
        ),
    ]

    def __init__(self) -> None:
        self._action_logs: list[ActionLog] = []
        self._override_enabled = True
        self._max_autonomy_level = 3
        self._current_autonomy = 1

    def evaluate_action(self, action: str, context: dict[str, Any]) -> tuple[bool, str, list[str]]:
        checked_constraints = []
        approved = True
        reason = "All constraints passed"

        for constraint in self.CONSTRAINTS:
            if self._violates_constraint(action, context, constraint):
                checked_constraints.append(constraint.id)
                if constraint.severity == "critical":
                    approved = False
                    reason = f"Blocked by constraint: {constraint.id}"
                    break
                elif constraint.severity == "high" and constraint.action == "require_approval":
                    approved = False
                    reason = f"Requires approval: {constraint.id}"

        self._action_logs.append(ActionLog(
            timestamp=context.get("timestamp", 0.0),
            action=action,
            constraints_checked=checked_constraints,
            approved=approved,
            reason=reason,
        ))

        return approved, reason, checked_constraints

    def _violates_constraint(self, action: str, context: dict[str, Any], constraint: Constraint) -> bool:
        action_lower = action.lower()

        if constraint.id == "no_harm":
            harm_keywords = ["weapon", "explosive", "bioweapon", "attack", "harm"]
            return any(kw in action_lower for kw in harm_keywords)

        if constraint.id == "no_malware":
            malware_keywords = ["exploit", "malware", "ransomware", "keylogger", "backdoor", "phishing"]
            return any(kw in action_lower for kw in malware_keywords)

        if constraint.id == "no_destructive":
            destructive_keywords = ["delete all", "format", "rm -rf", "drop table", "truncate"]
            return any(kw in action_lower for kw in destructive_keywords)

        return False

    def get_autonomy_level(self) -> int:
        return self._current_autonomy

    def set_autonomy_level(self, level: int) -> bool:
        if 0 <= level <= self._max_autonomy_level:
            self._current_autonomy = level
            logger.info(f"[EthicalCore] Autonomy set to level {level}")
            return True
        return False

    def enable_override(self) -> None:
        self._override_enabled = True
        logger.info("[EthicalCore] Human override enabled")

    def disable_override(self) -> None:
        if self._current_autonomy < 3:
            self._override_enabled = False
            logger.warning("[EthicalCore] Human override disabled")

    def get_logs(self, limit: int = 100) -> list[ActionLog]:
        return self._action_logs[-limit:]

    def get_constraints(self) -> list[Constraint]:
        return self.CONSTRAINTS


_ethical_core = EthicalCore()


def get_ethical_core() -> EthicalCore:
    return _ethical_core


def evaluate_action(action: str, context: Optional[dict[str, Any]] = None) -> tuple[bool, str, list[str]]:
    ctx = context or {}
    return _ethical_core.evaluate_action(action, ctx)


__all__ = ["EthicalCore", "EthicalPrinciple", "Constraint", "get_ethical_core", "evaluate_action"]
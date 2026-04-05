"""
HoloOS Planner and Reasoning System
===================================
Goal decomposition, planning, and multi-step reasoning.
"""

from __future__ import annotations

import logging
import time
import json
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

logger = logging.getLogger(__name__)


class GoalStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    PAUSED = auto()


class ReasoningStrategy(Enum):
    CHAIN_OF_THOUGHT = auto()
    TREE_OF_THOUGHT = auto()
    REACT = auto()
    REFLEXION = auto()
    REASONING = auto()
    MONTE_CARLO = auto()


@dataclass
class Goal:
    id: str
    description: str
    status: GoalStatus = GoalStatus.PENDING
    priority: int = 5
    created_at: float = field(default_factory=time.time)
    deadline: Optional[float] = None
    context: dict[str, Any] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)


@dataclass
class PlanStep:
    id: str
    description: str
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)
    status: GoalStatus = GoalStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class Plan:
    id: str
    goal_id: str
    steps: list[PlanStep] = field(default_factory=list)
    current_step: int = 0
    status: GoalStatus = GoalStatus.PENDING
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None


class GoalDecomposer:
    """Decomposes high-level goals into actionable steps."""

    def __init__(self) -> None:
        self._decomposition_rules: list[dict] = []
        logger.info("[GoalDecomposer] Initialized")

    def decompose(self, goal: str, context: dict = None) -> list[dict]:
        ctx = context or {}
        
        steps = []
        
        if "create" in goal.lower() or "build" in goal.lower():
            steps.append({"action": "analyze_requirements", "description": "Analyze requirements"})
            steps.append({"action": "design_solution", "description": "Design solution"})
            steps.append({"action": "implement", "description": "Implement solution"})
            steps.append({"action": "verify", "description": "Verify implementation"})
        
        elif "research" in goal.lower() or "find" in goal.lower():
            steps.append({"action": "define_search_query", "description": "Define search query"})
            steps.append({"action": "search", "description": "Search for information"})
            steps.append({"action": "analyze_results", "description": "Analyze results"})
            steps.append({"action": "synthesize", "description": "Synthesize findings"})
        
        elif "solve" in goal.lower() or "fix" in goal.lower():
            steps.append({"action": "identify_problem", "description": "Identify the problem"})
            steps.append({"action": "analyze_root_cause", "description": "Analyze root cause"})
            steps.append({"action": "generate_solution", "description": "Generate solution"})
            steps.append({"action": "implement_fix", "description": "Implement fix"})
            steps.append({"action": "verify", "description": "Verify fix"})
        
        elif "write" in goal.lower() or "generate" in goal.lower():
            steps.append({"action": "plan_structure", "description": "Plan structure"})
            steps.append({"action": "write_content", "description": "Write content"})
            steps.append({"action": "review", "description": "Review and refine"})
        
        else:
            steps.append({"action": "understand_goal", "description": "Understand goal"})
            steps.append({"action": "break_down", "description": "Break down into parts"})
            steps.append({"action": "execute_parts", "description": "Execute parts"})
            steps.append({"action": "combine_results", "description": "Combine results"})
        
        logger.debug(f"[GoalDecomposer] Decomposed into {len(steps)} steps")
        return steps


class ReasoningEngine:
    """Multi-strategy reasoning engine."""

    def __init__(self) -> None:
        self.strategies = {
            ReasoningStrategy.CHAIN_OF_THOUGHT: self._chain_of_thought,
            ReasoningStrategy.TREE_OF_THOUGHT: self._tree_of_thought,
            ReasoningStrategy.REACT: self._react,
        }
        self._reasoning_history: deque = deque(maxlen=100)
        logger.info("[ReasoningEngine] Initialized")

    def reason(
        self,
        problem: str,
        context: dict = None,
        strategy: ReasoningStrategy = ReasoningStrategy.CHAIN_OF_THOUGHT,
    ) -> dict[str, Any]:
        reasoning_fn = self.strategies.get(strategy, self._chain_of_thought)
        result = reasoning_fn(problem, context or {})
        
        self._reasoning_history.append({
            "problem": problem,
            "strategy": strategy.name,
            "result": result,
            "timestamp": time.time(),
        })
        
        return result

    def _chain_of_thought(self, problem: str, context: dict) -> dict[str, Any]:
        thoughts = []
        
        thoughts.append({
            "step": 1,
            "thought": f"Analyzing the problem: {problem[:50]}...",
            "confidence": 0.8,
        })
        
        thoughts.append({
            "step": 2,
            "thought": "Breaking down into logical components...",
            "confidence": 0.85,
        })
        
        thoughts.append({
            "step": 3,
            "thought": "Identifying relevant knowledge from context...",
            "confidence": 0.7,
        })
        
        thoughts.append({
            "step": 4,
            "thought": "Synthesizing solution...",
            "confidence": 0.9,
        })
        
        return {
            "strategy": "chain_of_thought",
            "thoughts": thoughts,
            "final_answer": f"Reasoned solution for: {problem[:30]}...",
            "confidence": 0.85,
        }

    def _tree_of_thought(self, problem: str, context: dict) -> dict[str, Any]:
        branches = []
        
        branches.append({
            "branch": "A",
            "approach": "Direct solution",
            "steps": ["Analyze problem", "Apply direct method", "Verify"],
            "feasibility": 0.8,
        })
        
        branches.append({
            "branch": "B",
            "approach": "Alternative approach",
            "steps": ["Restate problem", "Try different method", "Compare results"],
            "feasibility": 0.6,
        })
        
        return {
            "strategy": "tree_of_thought",
            "branches": branches,
            "selected_branch": "A",
            "final_answer": f"Best path identified for: {problem[:30]}...",
            "confidence": 0.8,
        }

    def _react(self, problem: str, context: dict) -> dict[str, Any]:
        actions = []
        
        actions.append({"action": "Observe", "observation": f"Problem: {problem[:50]}"})
        actions.append({"action": "Think", "thought": "Planning solution approach..."})
        actions.append({"action": "Act", "action": "Executing reasoning steps..."})
        actions.append({"action": "Reflect", "reflection": "Solution formulated"})
        
        return {
            "strategy": "react",
            "actions": actions,
            "final_answer": f"REACT solution for: {problem[:30]}...",
            "confidence": 0.85,
        }

    def get_history(self, limit: int = 10) -> list[dict]:
        return list(self._reasoning_history)[-limit:]


class Planner:
    """Main planner combining goal decomposition and reasoning."""

    def __init__(self) -> None:
        self.decomposer = GoalDecomposer()
        self.reasoning_engine = ReasoningEngine()
        
        self._goals: dict[str, Goal] = {}
        self._plans: dict[str, Plan] = {}
        
        logger.info("[Planner] Initialized")

    def create_goal(
        self,
        description: str,
        priority: int = 5,
        deadline: Optional[float] = None,
        context: dict = None,
    ) -> Goal:
        goal_id = f"goal_{len(self._goals)}_{int(time.time())}"
        
        goal = Goal(
            id=goal_id,
            description=description,
            priority=priority,
            deadline=deadline,
            context=context or {},
        )
        
        self._goals[goal_id] = goal
        logger.info(f"[Planner] Goal created: {goal_id}")
        
        return goal

    def create_plan(self, goal: Goal, context: dict = None) -> Plan:
        steps = self.decomposer.decompose(goal.description, context)
        
        plan_id = f"plan_{goal.id}"
        
        plan_steps = []
        for i, step in enumerate(steps):
            plan_steps.append(PlanStep(
                id=f"{plan_id}_step_{i}",
                description=step.get("description", ""),
                action=step.get("action", "unknown"),
                parameters=step.get("parameters", {}),
            ))
        
        plan = Plan(
            id=plan_id,
            goal_id=goal.id,
            steps=plan_steps,
        )
        
        self._plans[plan_id] = plan
        goal.status = GoalStatus.IN_PROGRESS
        
        logger.info(f"[Planner] Plan created: {plan_id} with {len(steps)} steps")
        
        return plan

    def execute_step(self, plan_id: str, executor_fn: Any = None) -> bool:
        if plan_id not in self._plans:
            return False
        
        plan = self._plans[plan_id]
        
        if plan.current_step >= len(plan.steps):
            plan.status = GoalStatus.COMPLETED
            plan.completed_at = time.time()
            return False
        
        step = plan.steps[plan.current_step]
        
        step.status = GoalStatus.IN_PROGRESS
        start_time = time.time()
        
        if executor_fn:
            try:
                step.result = executor_fn(step)
                step.status = GoalStatus.COMPLETED
            except Exception as e:
                step.error = str(e)
                step.status = GoalStatus.FAILED
        else:
            step.result = f"Executed: {step.action}"
            step.status = GoalStatus.COMPLETED
        
        step.execution_time = time.time() - start_time
        plan.current_step += 1
        
        if plan.current_step >= len(plan.steps):
            plan.status = GoalStatus.COMPLETED
            plan.completed_at = time.time()
            if plan.goal_id in self._goals:
                self._goals[plan.goal_id].status = GoalStatus.COMPLETED
        
        logger.debug(f"[Planner] Step executed: {step.id}")
        return plan.current_step < len(plan.steps)

    def get_next_action(self, plan_id: str) -> Optional[str]:
        if plan_id not in self._plans:
            return None
        
        plan = self._plans[plan_id]
        
        if plan.current_step < len(plan.steps):
            return plan.steps[plan.current_step].action
        
        return None

    def get_goal_status(self, goal_id: str) -> Optional[dict]:
        if goal_id not in self._goals:
            return None
        
        goal = self._goals[goal_id]
        
        return {
            "id": goal.id,
            "description": goal.description,
            "status": goal.status.name,
            "priority": goal.priority,
            "plan_id": f"plan_{goal.id}" if f"plan_{goal.id}" in self._plans else None,
        }

    def get_all_goals(self) -> list[dict]:
        return [
            {"id": g.id, "description": g.description, "status": g.status.name, "priority": g.priority}
            for g in self._goals.values()
        ]

    def reset(self) -> None:
        self._goals.clear()
        self._plans.clear()
        logger.info("[Planner] Reset")


_planner: Optional[Planner] = None


def get_planner() -> Planner:
    global _planner
    if _planner is None:
        _planner = Planner()
    return _planner


__all__ = [
    "GoalStatus",
    "ReasoningStrategy",
    "Goal",
    "PlanStep",
    "Plan",
    "GoalDecomposer",
    "ReasoningEngine",
    "Planner",
    "get_planner",
]
"""
HoloOS Autonomous Code Generator
=================================
Safe autonomous code generation with ethical guardrails.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Optional
from dataclasses import dataclass, field

from holoos.core.ethical import get_ethical_core, EthicalCore

logger = logging.getLogger(__name__)


@dataclass
class CodeGenerationRequest:
    language: str
    specification: str
    context: dict[str, Any] = field(default_factory=dict)
    autonomy_level: int = 1


@dataclass
class CodeGenerationResult:
    success: bool
    code: str
    explanation: str
    warnings: list[str] = field(default_factory=list)
    constraints_checked: list[str] = field(default_factory=list)


class AutonomousCodeGenerator:
    LANGUAGE_TEMPLATES = {
        "python": 'def {name}({params}):\n    """{docstring}"""\n    {body}',
        "rust": 'fn {name}({params}) -> {return_type} {{\n    {body}\n}}',
        "typescript": 'function {name}({params}): {return_type} {{\n    {body}\n}}',
        "javascript": 'function {name}({params}) {{\n    {body}\n}}',
        "go": 'func {name}({params}) {return_type} {{\n    {body}\n}}',
        "c": 'void {name}({params}) {{\n    {body}\n}}',
        "cpp": 'void {name}({params}) {{\n    {body}\n}}',
        "java": 'public void {name}({params}) {{\n    {body}\n}}',
        "csharp": 'public void {name}({params})\n{{\n    {body}\n}}',
        "swift": 'func {name}({params}) {{\n    {body}\n}}',
        "kotlin": 'fun {name}({params}) {{\n    {body}\n}}',
        "ruby": 'def {name}({params})\n    {body}\nend',
        "php": 'function {name}({params}) {{\n    {body}\n}}',
        "lua": 'function {name}({params})\n    {body}\nend',
        "scala": 'def {name}({params}): Unit = {{\n    {body}\n}}',
        "haskell": '{name} :: {type_signature}\n{name} {params} = {body}',
        "elixir": 'def {name}({params}) do\n    {body}\nend',
        "clojure": '(defn {name} [{params}]\n  {body})',
        "r": '{name} <- function({params}) {{\n    {body}\n}}',
        "julia": 'function {name}({params})\n    {body}\nend',
        "dart": 'void {name}({params}) {{\n    {body}\n}}',
        "zig": 'pub fn {name}({params}) void {{\n    {body}\n}}',
        "nim": 'proc {name}({params}) =\n    {body}',
        "crystal": 'def {name}({params})\n    {body}\nend',
        "perl": 'sub {name} {{\n    my ({params}) = @_;\n    {body}\n}}',
        "bash": '#!/bin/bash\nfunction {name}() {{\n    {body}\n}}',
    }

    def __init__(self, ethical_core: Optional[EthicalCore] = None) -> None:
        self.ethical_core = ethical_core or get_ethical_core()
        self._generation_history: list[CodeGenerationResult] = []

    def generate(self, request: CodeGenerationRequest) -> CodeGenerationResult:
        logger.info(f"[AutonomousCodeGenerator] Generating {request.language} code")
        
        approved, reason, checked = self.ethical_core.evaluate_action(
            f"generate_code:{request.specification[:50]}",
            {"language": request.language, "autonomy": request.autonomy_level}
        )
        
        if not approved:
            logger.warning(f"[AutonomousCodeGenerator] Code generation blocked: {reason}")
            return CodeGenerationResult(
                success=False,
                code="",
                explanation=f"Blocked: {reason}",
                constraints_checked=checked,
            )
        
        if request.autonomy_level > self.ethical_core.get_autonomy_level():
            return CodeGenerationResult(
                success=False,
                code="",
                explanation="Autonomy level exceeds permitted limit",
                constraints_checked=checked,
            )
        
        code = self._generate_code(request)
        
        warnings = self._check_code_safety(code, request.language)
        
        result = CodeGenerationResult(
            success=True,
            code=code,
            explanation=f"Generated {request.language} code from specification",
            warnings=warnings,
            constraints_checked=checked,
        )
        
        self._generation_history.append(result)
        return result

    def _generate_code(self, request: CodeGenerationRequest) -> str:
        template = self.LANGUAGE_TEMPLATES.get(request.language.lower(), self.LANGUAGE_TEMPLATES["python"])
        
        spec = request.specification.lower()
        
        if "function" in spec or "def" in spec:
            name_match = re.search(r'(?:named?|called?)\s+(\w+)', spec)
            name = name_match.group(1) if name_match else "generated_function"
        else:
            name = "generated_function"
        
        params_match = re.search(r'with\s+params?[:\s]+([^,\n]+)', spec)
        params = params_match.group(1) if params_match else ""
        
        docstring = f"Auto-generated function based on: {request.specification[:50]}"
        body = "    pass  # Implement based on specification"
        
        return template.format(
            name=name,
            params=params,
            docstring=docstring,
            body=body,
            return_type="void",
            type_signature="a -> b",
        )

    def _check_code_safety(self, code: str, language: str) -> list[str]:
        warnings = []
        
        dangerous_patterns = [
            (r'rm\s+-rf', "Contains potentially destructive command"),
            (r'exec\s*\(', "Contains dynamic execution"),
            (r'eval\s*\(', "Contains eval() - potential security risk"),
            (r'system\s*\(', "Contains system call"),
            (r'subprocess', "Contains subprocess call"),
        ]
        
        for pattern, warning in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                warnings.append(warning)
        
        return warnings

    def get_generation_history(self, limit: int = 50) -> list[CodeGenerationResult]:
        return self._generation_history[-limit:]


_code_generator: Optional[AutonomousCodeGenerator] = None


def get_code_generator() -> AutonomousCodeGenerator:
    global _code_generator
    if _code_generator is None:
        _code_generator = AutonomousCodeGenerator()
    return _code_generator


__all__ = ["AutonomousCodeGenerator", "CodeGenerationRequest", "CodeGenerationResult", "get_code_generator"]
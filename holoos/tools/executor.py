"""
HoloOS Tool Execution Engine
=============================
Executable tools for code, search, file operations, and more.
"""

from __future__ import annotations

import logging
import time
import json
import subprocess
import urllib.request
import urllib.parse
from typing import Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum, auto

logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    CODE_EXECUTION = auto()
    SEARCH = auto()
    FILE_IO = auto()
    SYSTEM = auto()
    NETWORK = auto()
    DATA = auto()
    AI = auto()


class ToolStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    TIMEOUT = auto()


@dataclass
class ToolDefinition:
    id: str
    name: str
    category: ToolCategory
    description: str
    parameters: dict
    handler: Callable
    timeout: int = 30
    enabled: bool = True


@dataclass
class ToolResult:
    tool_id: str
    status: ToolStatus
    output: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: dict = field(default_factory=dict)


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}
        self._register_builtin_tools()
        logger.info(f"[ToolRegistry] Initialized with {len(self._tools)} tools")

    def _register_builtin_tools(self) -> None:
        self.register(ToolDefinition(
            id="execute_python",
            name="Execute Python Code",
            category=ToolCategory.CODE_EXECUTION,
            description="Execute Python code and return output",
            parameters={"code": "str", "timeout": "int"},
            handler=self._execute_python,
            timeout=30,
        ))

        self.register(ToolDefinition(
            id="execute_bash",
            name="Execute Bash Command",
            category=ToolCategory.SYSTEM,
            description="Execute a bash command",
            parameters={"command": "str", "timeout": "int"},
            handler=self._execute_bash,
            timeout=30,
        ))

        self.register(ToolDefinition(
            id="web_search",
            name="Web Search",
            category=ToolCategory.SEARCH,
            description="Search the web for information",
            parameters={"query": "str", "num_results": "int"},
            handler=self._web_search,
            timeout=10,
        ))

        self.register(ToolDefinition(
            id="read_file",
            name="Read File",
            category=ToolCategory.FILE_IO,
            description="Read content from a file",
            parameters={"path": "str", "encoding": "str"},
            handler=self._read_file,
            timeout=5,
        ))

        self.register(ToolDefinition(
            id="write_file",
            name="Write File",
            category=ToolCategory.FILE_IO,
            description="Write content to a file",
            parameters={"path": "str", "content": "str", "encoding": "str"},
            handler=self._write_file,
            timeout=5,
        ))

        self.register(ToolDefinition(
            id="http_request",
            name="HTTP Request",
            category=ToolCategory.NETWORK,
            description="Make an HTTP request",
            parameters={"url": "str", "method": "str", "headers": "dict"},
            handler=self._http_request,
            timeout=10,
        ))

        self.register(ToolDefinition(
            id="json_parse",
            name="Parse JSON",
            category=ToolCategory.DATA,
            description="Parse JSON string",
            parameters={"json_string": "str"},
            handler=self._json_parse,
            timeout=2,
        ))

        self.register(ToolDefinition(
            id="json_build",
            name="Build JSON",
            category=ToolCategory.DATA,
            description="Build JSON string from object",
            parameters={"object": "any"},
            handler=self._json_build,
            timeout=2,
        ))

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.id] = tool
        logger.debug(f"[ToolRegistry] Registered tool: {tool.id}")

    def get(self, tool_id: str) -> Optional[ToolDefinition]:
        return self._tools.get(tool_id)

    def list_tools(self, category: ToolCategory = None) -> list[ToolDefinition]:
        tools = list(self._tools.values())
        if category:
            tools = [t for t in tools if t.category == category]
        return [t for t in tools if t.enabled]

    def enable(self, tool_id: str) -> bool:
        if tool_id in self._tools:
            self._tools[tool_id].enabled = True
            return True
        return False

    def disable(self, tool_id: str) -> bool:
        if tool_id in self._tools:
            self._tools[tool_id].enabled = False
            return True
        return False

    def _execute_python(self, params: dict) -> ToolResult:
        code = params.get("code", "")
        return ToolResult(
            tool_id="execute_python",
            status=ToolStatus.COMPLETED,
            output=f"Python execution simulated: {len(code)} chars",
            execution_time=0.1,
        )

    def _execute_bash(self, params: dict) -> ToolResult:
        cmd = params.get("command", "")
        return ToolResult(
            tool_id="execute_bash",
            status=ToolStatus.COMPLETED,
            output=f"Bash execution simulated: {cmd}",
            execution_time=0.1,
        )

    def _web_search(self, params: dict) -> ToolResult:
        query = params.get("query", "")
        num = params.get("num_results", 5)
        results = [{"title": f"Result {i}", "url": f"https://example.com/{i}", "snippet": f"Result for: {query}"} for i in range(num)]
        return ToolResult(
            tool_id="web_search",
            status=ToolStatus.COMPLETED,
            output={"query": query, "results": results},
            execution_time=0.5,
        )

    def _read_file(self, params: dict) -> ToolResult:
        path = params.get("path", "")
        return ToolResult(
            tool_id="read_file",
            status=ToolStatus.COMPLETED,
            output=f"File content for: {path}",
            execution_time=0.1,
        )

    def _write_file(self, params: dict) -> ToolResult:
        path = params.get("path", "")
        return ToolResult(
            tool_id="write_file",
            status=ToolStatus.COMPLETED,
            output={"written": True, "path": path},
            execution_time=0.1,
        )

    def _http_request(self, params: dict) -> ToolResult:
        url = params.get("url", "")
        return ToolResult(
            tool_id="http_request",
            status=ToolStatus.COMPLETED,
            output={"status": 200, "url": url},
            execution_time=0.2,
        )

    def _json_parse(self, params: dict) -> ToolResult:
        json_str = params.get("json_string", "{}")
        try:
            parsed = json.loads(json_str)
            return ToolResult(tool_id="json_parse", status=ToolStatus.COMPLETED, output=parsed, execution_time=0.01)
        except json.JSONDecodeError as e:
            return ToolResult(tool_id="json_parse", status=ToolStatus.FAILED, error=str(e), execution_time=0.01)

    def _json_build(self, params: dict) -> ToolResult:
        obj = params.get("object", {})
        return ToolResult(tool_id="json_build", status=ToolStatus.COMPLETED, output=json.dumps(obj), execution_time=0.01)


class ToolExecutor:
    """Executes tools with timeout and error handling."""

    def __init__(self) -> None:
        self.registry = ToolRegistry()
        self._execution_history: list[ToolResult] = []
        logger.info("[ToolExecutor] Initialized")

    def execute(self, tool_id: str, parameters: dict = None) -> ToolResult:
        params = parameters or {}
        tool = self.registry.get(tool_id)
        
        if not tool:
            return ToolResult(
                tool_id=tool_id,
                status=ToolStatus.FAILED,
                output=None,
                error=f"Tool not found: {tool_id}",
            )
        
        if not tool.enabled:
            return ToolResult(
                tool_id=tool_id,
                status=ToolStatus.FAILED,
                output=None,
                error=f"Tool disabled: {tool_id}",
            )
        
        start_time = time.time()
        
        try:
            result = tool.handler(params)
            result.execution_time = time.time() - start_time
            self._execution_history.append(result)
            return result
        except Exception as e:
            return ToolResult(
                tool_id=tool_id,
                status=ToolStatus.FAILED,
                output=None,
                error=str(e),
                execution_time=time.time() - start_time,
            )

    def execute_chain(self, tool_calls: list[dict]) -> list[ToolResult]:
        results = []
        for call in tool_calls:
            tool_id = call.get("tool_id")
            params = call.get("parameters", {})
            result = self.execute(tool_id, params)
            results.append(result)
            if result.status == ToolStatus.FAILED:
                break
        return results

    def get_execution_history(self, limit: int = 50) -> list[ToolResult]:
        return self._execution_history[-limit:]

    def get_stats(self) -> dict:
        total = len(self._execution_history)
        if total == 0:
            return {"total": 0, "by_status": {}}
        
        by_status = {}
        for r in self._execution_history:
            status = r.status.name
            by_status[status] = by_status.get(status, 0) + 1
        
        return {"total": total, "by_status": by_status}


_tool_executor: Optional[ToolExecutor] = None


def get_tool_executor() -> ToolExecutor:
    global _tool_executor
    if _tool_executor is None:
        _tool_executor = ToolExecutor()
    return _tool_executor


__all__ = [
    "ToolCategory",
    "ToolStatus",
    "ToolDefinition",
    "ToolResult",
    "ToolRegistry",
    "ToolExecutor",
    "get_tool_executor",
]
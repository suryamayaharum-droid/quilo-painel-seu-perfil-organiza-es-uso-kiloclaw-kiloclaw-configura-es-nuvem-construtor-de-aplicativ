"""
HoloOS AI Agent Engine
======================
High-capability AI agent with tools, memory, and multi-model support.
"""

from __future__ import annotations

import logging
import json
from typing import Any, Optional
from dataclasses import dataclass, field

from holoos.core.types import AgentConfig
from holoos.core.registry import ComponentRegistry, get_registry, register_tool

logger = logging.getLogger(__name__)


@dataclass
class AgentState:
    messages: list[dict[str, Any]] = field(default_factory=list)
    memory: dict[str, Any] = field(default_factory=dict)
    tools_used: list[str] = field(default_factory=list)


class Tool:
    name: str = ""
    description: str = ""

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


@register_tool("execute_code")
def execute_code(code: str, language: str = "python") -> dict[str, Any]:
    result = {
        "status": "simulated",
        "language": language,
        "code": code[:100],
        "output": f"Simulated execution of {len(code)} chars",
    }
    logger.info(f"[Tool] execute_code: {language}")
    return result


@register_tool("search_web")
def search_web(query: str, num_results: int = 5) -> dict[str, Any]:
    result = {
        "status": "simulated",
        "query": query,
        "results": [{"title": f"Result {i}", "url": f"https://example.com/{i}"} for i in range(num_results)],
    }
    logger.info(f"[Tool] search_web: {query}")
    return result


@register_tool("read_file")
def read_file(path: str) -> dict[str, Any]:
    result = {"status": "simulated", "path": path, "content": f"Content of {path}"}
    logger.info(f"[Tool] read_file: {path}")
    return result


@register_tool("write_file")
def write_file(path: str, content: str) -> dict[str, Any]:
    result = {"status": "simulated", "path": path, "bytes_written": len(content)}
    logger.info(f"[Tool] write_file: {path}")
    return result


@register_tool("run_command")
def run_command(command: str) -> dict[str, Any]:
    result = {"status": "simulated", "command": command, "output": f"Simulated: {command}"}
    logger.info(f"[Tool] run_command: {command}")
    return result


class AgentEngine:
    DEFAULT_TOOLS = [execute_code, search_web, read_file, write_file, run_command]

    def __init__(self, registry: Optional[ComponentRegistry] = None) -> None:
        self.registry = registry or get_registry()
        self._tools: dict[str, Any] = {}
        self._agents: dict[str, AgentState] = {}
        for tool_func in self.DEFAULT_TOOLS:
            self._tools[tool_func.__name__] = tool_func

        for tool_name in self.registry.list_tools():
            tool_func = self.registry.get_tool(tool_name)
            if tool_func:
                self._tools[tool_name] = tool_func

    def create_agent(self, config: AgentConfig) -> AgentState:
        state = AgentState()
        self._agents[config.name] = state
        logger.info(f"[AgentEngine] Created agent: {config.name}")
        return state

    def execute(self, prompt: str, config: AgentConfig) -> dict[str, Any]:
        if config.name not in self._agents:
            self.create_agent(config)

        state = self._agents[config.name]
        state.messages.append({"role": "user", "content": prompt})

        response_content = self._simulate_response(prompt, config)
        state.messages.append({"role": "assistant", "content": response_content})

        result = {
            "agent": config.name,
            "model": config.model,
            "response": response_content,
            "tools_used": state.tools_used,
            "message_count": len(state.messages),
        }
        logger.info(f"[AgentEngine] Executed: {config.name}, tools: {len(state.tools_used)}")
        return result

    def _simulate_response(self, prompt: str, config: AgentConfig) -> str:
        if "code" in prompt.lower() or "write" in prompt.lower():
            return "```python\ndef hello():\n    print('Hello from HoloOS Agent!')\n```"
        elif "search" in prompt.lower() or "find" in prompt.lower():
            return "Here are some search results for your query..."
        else:
            return f"HoloOS Agent response (model: {config.model}, temp: {config.temperature})"

    def add_tool(self, tool: Tool) -> None:
        self._tools[tool.name] = tool
        logger.info(f"[AgentEngine] Added tool: {tool.name}")

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def get_agent_state(self, name: str) -> Optional[AgentState]:
        return self._agents.get(name)
"""
HoloOS Function Calling
=======================
Tool calling capabilities for AI models.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class FunctionCallStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class FunctionDefinition:
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Optional[Callable] = None


@dataclass
class FunctionCall:
    id: str
    function: str
    arguments: Dict[str, Any]
    status: FunctionCallStatus = FunctionCallStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None


class FunctionRegistry:
    def __init__(self):
        self.functions: Dict[str, FunctionDefinition] = {}
        self._register_default_functions()
    
    def _register_default_functions(self):
        self.register(
            FunctionDefinition(
                name="get_weather",
                description="Get weather information for a location",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"},
                        "units": {"type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius"}
                    },
                    "required": ["location"]
                }
            )
        )
        
        self.register(
            FunctionDefinition(
                name="calculate",
                description="Perform mathematical calculations",
                parameters={
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "Math expression"}
                    },
                    "required": ["expression"]
                }
            )
        )
        
        self.register(
            FunctionDefinition(
                name="search_code",
                description="Search for code in the codebase",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "language": {"type": "string", "description": "Programming language"}
                    },
                    "required": ["query"]
                }
            )
        )
        
        self.register(
            FunctionDefinition(
                name="create_file",
                description="Create a new file with content",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"},
                        "content": {"type": "string", "description": "File content"}
                    },
                    "required": ["path", "content"]
                }
            )
        )
        
        self.register(
            FunctionDefinition(
                name="execute_command",
                description="Execute a shell command",
                parameters={
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to execute"},
                        "timeout": {"type": "integer", "default": 30}
                    },
                    "required": ["command"]
                }
            )
        )
    
    def register(self, function: FunctionDefinition):
        self.functions[function.name] = function
    
    def get(self, name: str) -> Optional[FunctionDefinition]:
        return self.functions.get(name)
    
    def list_functions(self) -> List[FunctionDefinition]:
        return list(self.functions.values())
    
    def get_schemas(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": f.name,
                    "description": f.description,
                    "parameters": f.parameters
                }
            }
            for f in self.functions.values()
        ]


class FunctionExecutor:
    def __init__(self, registry: FunctionRegistry):
        self.registry = registry
    
    async def execute(self, call: FunctionCall) -> FunctionCall:
        function = self.registry.get(call.function)
        
        if not function:
            call.status = FunctionCallStatus.ERROR
            call.error = f"Function {call.function} not found"
            return call
        
        call.status = FunctionCallStatus.RUNNING
        
        try:
            if function.handler:
                call.result = await function.handler(call.arguments)
            else:
                call.result = self._default_handler(call.function, call.arguments)
            
            call.status = FunctionCallStatus.SUCCESS
        except Exception as e:
            call.status = FunctionCallStatus.ERROR
            call.error = str(e)
        
        return call
    
    def _default_handler(self, function: str, args: Dict[str, Any]) -> Any:
        handlers = {
            "get_weather": lambda a: f"Weather in {a.get('location')}: 22°C, sunny",
            "calculate": lambda a: eval(a.get("expression", "0")),
            "search_code": lambda a: f"Found 0 results for '{a.get('query')}'",
            "create_file": lambda a: f"Created file: {a.get('path')}",
            "execute_command": lambda a: f"Executed: {a.get('command')}",
        }
        
        handler = handlers.get(function)
        return handler(args) if handler else "Function executed"


def create_function_call(function: str, arguments: Dict[str, Any]) -> FunctionCall:
    return FunctionCall(
        id=f"call_{hash(str(arguments)) % 100000}",
        function=function,
        arguments=arguments
    )


# Singleton
_function_registry = FunctionRegistry()
_function_executor = FunctionExecutor(_function_registry)


def get_function_registry() -> FunctionRegistry:
    return _function_registry


def get_function_executor() -> FunctionExecutor:
    return _function_executor


__all__ = [
    "FunctionDefinition",
    "FunctionCall",
    "FunctionCallStatus",
    "FunctionRegistry",
    "FunctionExecutor",
    "get_function_registry",
    "get_function_executor",
    "create_function_call"
]
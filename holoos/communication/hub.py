"""
HoloOS Communication Layer
==========================
HTTP, WebSocket, and gRPC communication interfaces.
"""

from __future__ import annotations

import logging
import json
import time
from typing import Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

logger = logging.getLogger(__name__)


class Protocol(Enum):
    HTTP = auto()
    WEBSOCKET = auto()
    GRPC = auto()
    WEBSUB = auto()


class MessageType(Enum):
    REQUEST = auto()
    RESPONSE = auto()
    EVENT = auto()
    STREAM = auto()
    BROADCAST = auto()


class ConnectionStatus(Enum):
    CONNECTED = auto()
    DISCONNECTED = auto()
    CONNECTING = auto()
    ERROR = auto()


@dataclass
class Message:
    id: str
    type: MessageType
    protocol: Protocol
    sender: str
    receiver: str
    payload: Any
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)


@dataclass
class Endpoint:
    path: str
    method: str
    handler: Callable
    description: str = ""
    auth_required: bool = False


@dataclass
class ClientConnection:
    id: str
    status: ConnectionStatus
    protocol: Protocol
    connected_at: float
    last_activity: float
    metadata: dict = field(default_factory=dict)


class RequestRouter:
    """HTTP request router."""

    def __init__(self) -> None:
        self._endpoints: dict[str, Endpoint] = {}
        self._middleware: list[Callable] = []
        logger.info("[RequestRouter] Initialized")

    def register(self, path: str, method: str, handler: Callable, description: str = "") -> None:
        key = f"{method}:{path}"
        self._endpoints[key] = Endpoint(
            path=path,
            method=method,
            handler=handler,
            description=description,
        )
        logger.debug(f"[RequestRouter] Registered: {key}")

    def route(self, path: str, method: str, data: Any = None) -> Any:
        key = f"{method}:{path}"
        
        if key not in self._endpoints:
            for endpoint_key, endpoint in self._endpoints.items():
                if self._match_path(endpoint.path, path):
                    key = endpoint_key
                    break
        
        if key not in self._endpoints:
            return {"error": "Not found", "status": 404}
        
        endpoint = self._endpoints[key]
        
        for middleware in self._middleware:
            if not middleware(path, method):
                return {"error": "Forbidden", "status": 403}
        
        try:
            result = endpoint.handler(data) if data else endpoint.handler()
            return {"data": result, "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}

    def _match_path(self, pattern: str, path: str) -> bool:
        if pattern == path:
            return True
        if "{param}" in pattern:
            pattern_parts = pattern.split("/")
            path_parts = path.split("/")
            if len(pattern_parts) != len(path_parts):
                return False
            for i, part in enumerate(pattern_parts):
                if part != path_parts[i] and "{" not in part:
                    return False
            return True
        return False

    def add_middleware(self, middleware: Callable) -> None:
        self._middleware.append(middleware)


class WebSocketManager:
    """WebSocket connection manager."""

    def __init__(self) -> None:
        self._connections: dict[str, ClientConnection] = {}
        self._subscribers: dict[str, set[str]] = {}
        self._message_queue: deque = deque(maxlen=1000)
        logger.info("[WebSocketManager] Initialized")

    def connect(self, client_id: str, metadata: dict = None) -> ClientConnection:
        connection = ClientConnection(
            id=client_id,
            status=ConnectionStatus.CONNECTED,
            protocol=Protocol.WEBSOCKET,
            connected_at=time.time(),
            last_activity=time.time(),
            metadata=metadata or {},
        )
        self._connections[client_id] = connection
        logger.info(f"[WebSocketManager] Client connected: {client_id}")
        return connection

    def disconnect(self, client_id: str) -> bool:
        if client_id in self._connections:
            self._connections[client_id].status = ConnectionStatus.DISCONNECTED
            del self._connections[client_id]
            
            for topic in self._subscribers:
                self._subscribers[topic].discard(client_id)
            
            logger.info(f"[WebSocketManager] Client disconnected: {client_id}")
            return True
        return False

    def subscribe(self, client_id: str, topic: str) -> None:
        if topic not in self._subscribers:
            self._subscribers[topic] = set()
        self._subscribers[topic].add(client_id)
        logger.debug(f"[WebSocketManager] {client_id} subscribed to {topic}")

    def unsubscribe(self, client_id: str, topic: str) -> None:
        if topic in self._subscribers:
            self._subscribers[topic].discard(client_id)

    def send(self, client_id: str, message: Any) -> bool:
        if client_id not in self._connections:
            return False
        
        self._connections[client_id].last_activity = time.time()
        self._message_queue.append({
            "to": client_id,
            "message": message,
            "timestamp": time.time(),
        })
        return True

    def broadcast(self, topic: str, message: Any) -> int:
        if topic not in self._subscribers:
            return 0
        
        count = 0
        for client_id in self._subscribers[topic]:
            if self.send(client_id, message):
                count += 1
        
        return count

    def get_connected_clients(self) -> list[dict]:
        return [
            {
                "id": c.id,
                "status": c.status.name,
                "connected_at": c.connected_at,
                "last_activity": c.last_activity,
            }
            for c in self._connections.values()
            if c.status == ConnectionStatus.CONNECTED
        ]


class EventBus:
    """Event-driven communication bus."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable]] = {}
        self._event_history: deque = deque(maxlen=500)
        logger.info("[EventBus] Initialized")

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.debug(f"[EventBus] Handler subscribed to: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)

    def publish(self, event_type: str, data: Any, source: str = "system") -> list[Any]:
        event = {
            "type": event_type,
            "data": data,
            "source": source,
            "timestamp": time.time(),
        }
        
        self._event_history.append(event)
        
        results = []
        handlers = self._handlers.get(event_type, [])
        
        for handler in handlers:
            try:
                result = handler(data)
                results.append(result)
            except Exception as e:
                logger.error(f"[EventBus] Handler error: {e}")
        
        return results

    def get_event_history(self, event_type: str = None, limit: int = 50) -> list[dict]:
        events = list(self._event_history)
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        return events[-limit:]


class CommunicationHub:
    """
    Unified communication hub integrating all protocols.
    """

    def __init__(self) -> None:
        self.router = RequestRouter()
        self.ws_manager = WebSocketManager()
        self.event_bus = EventBus()
        
        self._default_handlers()
        
        logger.info("[CommunicationHub] Initialized")

    def _default_handlers(self) -> None:
        self.router.register("/health", "GET", lambda: {"status": "ok", "timestamp": time.time()})
        self.router.register("/status", "GET", self._get_status)
        self.router.register("/clients", "GET", self._get_clients)

    def _get_status(self, data: Any = None) -> dict:
        return {
            "http_endpoints": len(self.router._endpoints),
            "ws_connections": len(self.ws_manager.get_connected_clients()),
            "event_handlers": len(self.router._endpoints),
            "timestamp": time.time(),
        }

    def _get_clients(self, data: Any = None) -> dict:
        return {"clients": self.ws_manager.get_connected_clients()}

    def handle_http_request(self, path: str, method: str, data: Any = None) -> Any:
        return self.router.route(path, method, data)

    def handle_websocket_message(self, client_id: str, message: Any) -> Any:
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                message = {"raw": message}
        
        event_type = message.get("type", "default")
        return self.event_bus.publish(f"ws:{event_type}", message, client_id)

    def emit_event(self, event_type: str, data: Any) -> list[Any]:
        return self.event_bus.publish(event_type, data)

    def on_event(self, event_type: str, handler: Callable) -> None:
        self.event_bus.subscribe(event_type, handler)


_communication_hub: Optional[CommunicationHub] = None


def get_communication_hub() -> CommunicationHub:
    global _communication_hub
    if _communication_hub is None:
        _communication_hub = CommunicationHub()
    return _communication_hub


__all__ = [
    "Protocol",
    "MessageType",
    "ConnectionStatus",
    "Message",
    "Endpoint",
    "ClientConnection",
    "RequestRouter",
    "WebSocketManager",
    "EventBus",
    "CommunicationHub",
    "get_communication_hub",
]
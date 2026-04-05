"""
HoloOS Webhooks System
======================
Webhook events for external integrations.
"""

from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
import hashlib
import hmac
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("holoos-webhooks")


@dataclass
class WebhookEvent:
    id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: str
    retry_count: int = 0


class WebhookManager:
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or "webhook-secret-key"
        self.subscribers: Dict[str, List[str]] = {}
        self.events: List[WebhookEvent] = []
        self.handlers: Dict[str, Callable] = {}
    
    def register_webhook(self, url: str, events: List[str]) -> bool:
        for event_type in events:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            if url not in self.subscribers[event_type]:
                self.subscribers[event_type].append(url)
                logger.info(f"Registered webhook {url} for {event_type}")
        return True
    
    def unregister_webhook(self, url: str) -> bool:
        for event_type in self.subscribers:
            if url in self.subscribers[event_type]:
                self.subscribers[event_type].remove(url)
        return True
    
    def trigger_event(self, event_type: str, payload: Dict[str, Any]) -> WebhookEvent:
        event = WebhookEvent(
            id=f"evt_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}",
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now().isoformat()
        )
        
        self.events.append(event)
        
        urls = self.subscribers.get(event_type, [])
        for url in urls:
            self._send_webhook(url, event)
        
        return event
    
    def _send_webhook(self, url: str, event: WebhookEvent):
        logger.info(f"Sending webhook {event.event_type} to {url}")
    
    def sign_payload(self, payload: str) -> str:
        return hmac.new(
            self.secret_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        expected = self.sign_payload(payload)
        return hmac.compare_digest(expected, signature)
    
    def get_events(self, event_type: Optional[str] = None, limit: int = 50) -> List[WebhookEvent]:
        if event_type:
            return [e for e in self.events if e.event_type == event_type][-limit:]
        return self.events[-limit:]
    
    def register_handler(self, event_type: str, handler: Callable):
        self.handlers[event_type] = handler
    
    def process_event(self, event_type: str, payload: Dict[str, Any]):
        handler = self.handlers.get(event_type)
        if handler:
            handler(payload)


# Predefined event types
class WebhookEvents:
    CHAT_MESSAGE = "chat.message"
    MEMORY_STORED = "memory.stored"
    GOAL_CREATED = "goal.created"
    TOOL_EXECUTED = "tool.executed"
    SECURITY_ALERT = "security.alert"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    SYSTEM_ERROR = "system.error"


# Singleton instance
_webhook_manager = WebhookManager()


def get_webhook_manager() -> WebhookManager:
    return _webhook_manager


__all__ = ["WebhookManager", "WebhookEvent", "WebhookEvents", "get_webhook_manager"]
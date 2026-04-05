"""
HoloOS OpenTelemetry Tracing
=============================
Distributed tracing for request tracking.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import time
import uuid
import json


@dataclass
class Span:
    trace_id: str
    span_id: str
    parent_id: Optional[str]
    name: str
    service: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: str = "ok"
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)


class TraceContext:
    def __init__(self):
        self.spans: List[Span] = []
        self.current_span: Optional[Span] = None
    
    def create_span(self, name: str, service: str, parent_id: Optional[str] = None) -> Span:
        trace_id = self.current_span.trace_id if self.current_span else str(uuid.uuid4())
        span_id = str(uuid.uuid4())[:16]
        
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_id=parent_id or (self.current_span.span_id if self.current_span else None),
            name=name,
            service=service
        )
        
        self.current_span = span
        self.spans.append(span)
        
        return span
    
    def end_span(self, span: Span, status: str = "ok"):
        span.end_time = time.time()
        span.status = status
        
        if self.current_span == span:
            self.current_span = None
    
    def add_event(self, name: str, attributes: Dict[str, Any] = None):
        if self.current_span:
            self.current_span.events.append({
                "name": name,
                "timestamp": time.time(),
                "attributes": attributes or {}
            })
    
    def add_attribute(self, key: str, value: Any):
        if self.current_span:
            self.current_span.attributes[key] = value
    
    def to_json(self) -> List[Dict[str, Any]]:
        return [
            {
                "trace_id": s.trace_id,
                "span_id": s.span_id,
                "parent_id": s.parent_id,
                "name": s.name,
                "service": s.service,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "duration": s.end_time - s.start_time if s.end_time else None,
                "status": s.status,
                "attributes": s.attributes,
                "events": s.events
            }
            for s in self.spans
        ]


class Tracing:
    def __init__(self, service_name: str = "holoos"):
        self.service_name = service_name
        self.context = TraceContext()
    
    def start_trace(self, operation: str) -> Span:
        return self.context.create_span(operation, self.service_name)
    
    def start_child_span(self, name: str) -> Span:
        return self.context.create_span(name, self.service_name)
    
    def end_trace(self, span: Span, status: str = "ok"):
        self.context.end_span(span, status)
    
    def record_event(self, name: str, attributes: Dict[str, Any] = None):
        self.context.add_event(name, attributes)
    
    def set_attribute(self, key: str, value: Any):
        self.context.add_attribute(key, value)
    
    def get_traces(self) -> List[Dict[str, Any]]:
        return self.context.to_json()


# Decorator for automatic tracing
def traced(operation: str = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            tracer = Tracing()
            span = tracer.start_trace(operation or func.__name__)
            
            try:
                result = func(*args, **kwargs)
                tracer.end_trace(span, "ok")
                return result
            except Exception as e:
                tracer.set_attribute("error", str(e))
                tracer.end_trace(span, "error")
                raise
        
        return wrapper
    return decorator


# Context manager for spans
class SpanContext:
    def __init__(self, tracer: Tracing, name: str):
        self.tracer = tracer
        self.name = name
        self.span: Optional[Span] = None
    
    def __enter__(self):
        self.span = self.tracer.start_child_span(self.name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.tracer.set_attribute("error", str(exc_val))
            self.tracer.end_trace(self.span, "error")
        else:
            self.tracer.end_trace(self.span, "ok")


# Singleton tracer
_tracer = Tracing()


def get_tracer() -> Tracing:
    return _tracer


def create_span(name: str) -> Span:
    return _tracer.start_child_span(name)


__all__ = ["Tracing", "Span", "SpanContext", "traced", "get_tracer", "create_span", "TraceContext"]
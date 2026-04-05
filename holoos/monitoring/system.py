"""
HoloOS Monitoring and Metrics
============================
System monitoring, metrics collection, and health checks.
"""

from __future__ import annotations

import logging
import time
import psutil
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

logger = logging.getLogger(__name__)


class MetricType(Enum):
    COUNTER = auto()
    GAUGE = auto()
    HISTOGRAM = auto()
    TIMER = auto()


@dataclass
class Metric:
    name: str
    value: float
    metric_type: MetricType
    timestamp: float
    labels: dict = field(default_factory=dict)


class MetricsCollector:
    """Collects and stores system metrics."""

    def __init__(self) -> None:
        self._metrics: dict[str, deque] = {}
        logger.info("[MetricsCollector] Initialized")

    def record(self, name: str, value: float, metric_type: MetricType = MetricType.GAUGE, labels: dict = None) -> None:
        if name not in self._metrics:
            self._metrics[name] = deque(maxlen=1000)
        
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=time.time(),
            labels=labels or {},
        )
        self._metrics[name].append(metric)

    def increment(self, name: str, value: float = 1.0, labels: dict = None) -> None:
        self.record(name, value, MetricType.COUNTER, labels)

    def gauge(self, name: str, value: float, labels: dict = None) -> None:
        self.record(name, value, MetricType.GAUGE, labels)

    def timing(self, name: str, duration: float, labels: dict = None) -> None:
        self.record(name, duration, MetricType.TIMER, labels)

    def get(self, name: str, limit: int = 100) -> list[Metric]:
        if name in self._metrics:
            return list(self._metrics[name])[-limit:]
        return []

    def get_latest(self, name: str) -> Optional[float]:
        metrics = self.get(name, 1)
        return metrics[0].value if metrics else None


class HealthChecker:
    """System health checks."""

    def __init__(self) -> None:
        self._checks: dict[str, Callable] = {}
        self._register_default_checks()
        logger.info("[HealthChecker] Initialized")

    def _register_default_checks(self) -> None:
        self.register("cpu", self._check_cpu)
        self.register("memory", self._check_memory)
        self.register("disk", self._check_disk)

    def register(self, name: str, check_fn: Callable) -> None:
        self._checks[name] = check_fn

    def check_all(self) -> dict:
        results = {}
        for name, check_fn in self._checks.items():
            try:
                results[name] = check_fn()
            except Exception as e:
                results[name] = {"status": "error", "message": str(e)}
        return results

    def _check_cpu(self) -> dict:
        return {"status": "healthy", "cpu_percent": psutil.cpu_percent()}

    def _check_memory(self) -> dict:
        mem = psutil.virtual_memory()
        return {"status": "healthy" if mem.percent < 90 else "warning", "percent": mem.percent}

    def _check_disk(self) -> dict:
        disk = psutil.disk_usage("/")
        return {"status": "healthy" if disk.percent < 90 else "warning", "percent": disk.percent}


class Logger:
    """Structured logging."""

    def __init__(self, name: str = "holoos") -> None:
        self.logger = logging.getLogger(name)
        self._handlers: list[dict] = []
        logger.info(f"[Logger] Initialized: {name}")

    def log(self, level: str, message: str, **kwargs) -> None:
        extra = {"extra_data": kwargs}
        getattr(self.logger, level.lower())(message, extra=extra)

    def info(self, message: str, **kwargs) -> None:
        self.log("info", message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.log("error", message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self.log("warning", message, **kwargs)


class MonitoringSystem:
    """Main monitoring system."""

    def __init__(self) -> None:
        self.metrics = MetricsCollector()
        self.health = HealthChecker()
        self.logger = Logger()
        
        logger.info("[MonitoringSystem] Initialized")

    def record_request(self, endpoint: str, duration: float, status: int) -> None:
        self.metrics.timing(f"request.{endpoint}.duration", duration)
        self.metrics.increment(f"request.{endpoint}.count")
        self.metrics.increment(f"request.status.{status}")

    def get_status(self) -> dict:
        health = self.health.check_all()
        return {
            "health": health,
            "metrics_count": sum(len(v) for v in self.metrics._metrics.values()),
        }


_monitor: Optional[MonitoringSystem] = None


def get_monitoring() -> MonitoringSystem:
    global _monitor
    if _monitor is None:
        _monitor = MonitoringSystem()
    return _monitor


__all__ = [
    "MetricType",
    "Metric",
    "MetricsCollector",
    "HealthChecker",
    "Logger",
    "MonitoringSystem",
    "get_monitoring",
]
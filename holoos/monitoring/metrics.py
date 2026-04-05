"""
HoloOS Prometheus Metrics
=========================
Export metrics in Prometheus format.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import time


@dataclass
class Metric:
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    metric_type: str = "gauge"


class MetricsExporter:
    def __init__(self):
        self.metrics: Dict[str, List[Metric]] = {}
        self.counters: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        if name not in self.metrics:
            self.metrics[name] = []
        
        metric = Metric(
            name=name,
            value=value,
            labels=labels or {},
            metric_type="gauge"
        )
        self.metrics[name].append(metric)
    
    def counter(self, name: str, labels: Dict[str, str] = None):
        key = f"{name}:{str(labels)}"
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += 1
        
        self.gauge(f"{name}_total", self.counters[key], labels)
    
    def histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        if name not in self.histograms:
            self.histograms[name] = []
        
        self.histograms[name].append(value)
        
        buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        for bucket in buckets:
            count = sum(1 for v in self.histograms[name] if v <= bucket)
            self.gauge(f"{name}_bucket", count, {**(labels or {}), "le": str(bucket)})
        
        self.gauge(f"{name}_sum", sum(self.histograms[name]), labels)
        self.gauge(f"{name}_count", len(self.histograms[name]), labels)
    
    def increment(self, name: str, value: float = 1, labels: Dict[str, str] = None):
        self.gauge(name, value, labels)
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        self.gauge(name, value, labels)
    
    def to_prometheus(self) -> str:
        lines = []
        
        for name, metric_list in self.metrics.items():
            for metric in metric_list:
                labels_str = ",".join(f'{k}="{v}"' for k, v in metric.labels.items())
                
                if labels_str:
                    lines.append(f"{name}{{{labels_str}}} {metric.value}")
                else:
                    lines.append(f"{name} {metric.value}")
        
        return "\n".join(lines)
    
    def to_json(self) -> Dict[str, Any]:
        result = {}
        for name, metric_list in self.metrics.items():
            result[name] = [
                {
                    "value": m.value,
                    "labels": m.labels,
                    "timestamp": m.timestamp
                }
                for m in metric_list
            ]
        return result


# Predefined metrics
class HoloOSMetrics:
    def __init__(self):
        self.exporter = MetricsExporter()
    
    def record_request(self, endpoint: str, method: str, status: int):
        self.exporter.counter("holoos_requests_total", {"endpoint": endpoint, "method": method, "status": str(status)})
    
    def record_latency(self, endpoint: str, latency: float):
        self.exporter.histogram("holoos_request_latency_seconds", latency, {"endpoint": endpoint})
    
    def set_memory_usage(self, memory_type: str, items: int):
        self.exporter.set_gauge(f"holoos_memory_{memory_type}_items", items)
    
    def set_model_usage(self, model: str, active: bool):
        self.exporter.set_gauge("holoos_model_active", 1 if active else 0, {"model": model})
    
    def record_error(self, error_type: str):
        self.exporter.counter("holoos_errors_total", {"type": error_type})
    
    def set_security_level(self, level: str):
        level_map = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        self.exporter.set_gauge("holoos_security_level", level_map.get(level, 0))


_metrics = HoloOSMetrics()


def get_metrics() -> HoloOSMetrics:
    return _metrics


def get_prometheus_metrics() -> str:
    return _metrics.exporter.to_prometheus()


__all__ = ["MetricsExporter", "Metric", "HoloOSMetrics", "get_metrics", "get_prometheus_metrics"]
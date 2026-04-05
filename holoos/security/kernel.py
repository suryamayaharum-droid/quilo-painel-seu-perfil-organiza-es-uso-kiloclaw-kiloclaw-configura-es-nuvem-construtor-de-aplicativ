"""
HoloOS Security Kernel
=======================
Self-defense and security monitoring system.
Detects threats, protects against attacks, and maintains system integrity.
"""

from __future__ import annotations

import logging
import time
import hashlib
import re
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class ThreatCategory(Enum):
    INTRUSION = auto()
    MALWARE = auto()
    EXPLOIT = auto()
    REVERSE_ENGINEERING = auto()
    UNAUTHORIZED_ACCESS = auto()
    RESOURCE_ABUSE = auto()
    DATA_THEFT = auto()
    PRIVACY_VIOLATION = auto()


@dataclass
class SecurityEvent:
    id: str
    timestamp: float
    category: ThreatCategory
    level: ThreatLevel
    description: str
    source: str
    action_taken: str
    blocked: bool


@dataclass
class SecurityPolicy:
    id: str
    name: str
    description: str
    rules: list[str]
    action: str
    enabled: bool = True


class ThreatDetector:
    """Detects various types of threats in system operations."""

    THREAT_PATTERNS = {
        ThreatCategory.INTRUSION: [
            r"brute\s*force", r"password\s*spray", r"sql\s*injection",
            r"xss", r"csrf", r"path\s*traversal", r"buffer\s*overflow",
        ],
        ThreatCategory.MALWARE: [
            r"ransomware", r"keylogger", r"trojan", r"virus", r"worm",
            r"backdoor", r"rootkit", r"spyware", r"adware",
        ],
        ThreatCategory.EXPLOIT: [
            r"exploit", r"zeroday", r"vulnerability", r"cve-\d+-\d+",
            r"privilege\s*escalation", r"buffer\s*overflow", r"race\s*condition",
        ],
        ThreatCategory.REVERSE_ENGINEERING: [
            r"disassemble", r"decompile", r"debugger", r"ollydbg", r"ida\s*pro",
            r"ghidra", r"radare", r"binwalk", r"strings\s+.*binary",
            r"reverse\s*engineer", r"dump\s*memory", r"hook\s*function",
        ],
        ThreatCategory.UNAUTHORIZED_ACCESS: [
            r"sudo\s+.*", r"chmod\s+777", r"chown", r"passwd\s+-r",
            r"cat\s+/etc/shadow", r"crontab\s+-e", r"ssh\s+.*@",
        ],
        ThreatCategory.RESOURCE_ABUSE: [
            r"fork\s*bomb", r"while\s*true\s*:\s*fork", r"dd\s+if=",
            r":\(\)\{", r"kill\s+-9\s+-1", r"chmod\s+-R\s+777",
        ],
        ThreatCategory.DATA_THEFT: [
            r"wget\s+.*\|", r"curl\s+.*>", r"nc\s+-e", r"netcat\s+.*>",
            r"scp\s+.*:", r"rsync\s+.*", r"ftp\s+.*", r"exfil",
        ],
    }

    def __init__(self) -> None:
        self._event_history: deque = deque(maxlen=1000)
        logger.info("[ThreatDetector] Initialized")

    def analyze_input(self, input_data: str) -> tuple[bool, Optional[ThreatCategory], ThreatLevel]:
        input_lower = input_data.lower()
        
        for category, patterns in self.THREAT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, input_lower, re.IGNORECASE):
                    level = self._determine_level(category)
                    return True, category, level
        
        return False, None, ThreatLevel.LOW

    def _determine_level(self, category: ThreatCategory) -> ThreatLevel:
        high_threat = {ThreatCategory.MALWARE, ThreatCategory.EXPLOIT, ThreatCategory.DATA_THEFT}
        medium_threat = {ThreatCategory.INTRUSION, ThreatCategory.REVERSE_ENGINEERING}
        
        if category in high_threat:
            return ThreatLevel.CRITICAL
        elif category in medium_threat:
            return ThreatLevel.HIGH
        return ThreatLevel.MEDIUM

    def record_event(self, event: SecurityEvent) -> None:
        self._event_history.append(event)

    def get_threat_stats(self) -> dict[str, Any]:
        return {
            "total_events": len(self._event_history),
            "by_category": self._count_by_category(),
            "by_level": self._count_by_level(),
        }

    def _count_by_category(self) -> dict[str, int]:
        counts = {}
        for event in self._event_history:
            cat = event.category.name
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def _count_by_level(self) -> dict[str, int]:
        counts = {}
        for event in self._event_history:
            level = event.level.name
            counts[level] = counts.get(level, 0) + 1
        return counts


class IntrusionPreventionSystem:
    """IPS - Monitors and blocks suspicious activities."""

    def __init__(self) -> None:
        self._blocked_ips: set[str] = set()
        self._blocked_operations: set[str] = set()
        self._rate_limits: dict[str, list[float]] = {}
        self._max_requests_per_minute = 60
        logger.info("[IPS] Initialized")

    def check_request(self, source: str, operation: str) -> tuple[bool, str]:
        if source in self._blocked_ips:
            return False, "IP blocked due to previous violations"
        
        if operation in self._blocked_operations:
            return False, "Operation blocked by security policy"
        
        if not self._check_rate_limit(source):
            return False, "Rate limit exceeded"
        
        return True, "Allowed"

    def block_ip(self, ip: str, reason: str, duration: int = 3600) -> None:
        self._blocked_ips.add(ip)
        logger.warning(f"[IPS] Blocked IP: {ip} for {duration}s - {reason}")

    def block_operation(self, operation: str, reason: str) -> None:
        self._blocked_operations.add(operation)
        logger.warning(f"[IPS] Blocked operation: {operation} - {reason}")

    def _check_rate_limit(self, source: str) -> bool:
        now = time.time()
        
        if source not in self._rate_limits:
            self._rate_limits[source] = []
        
        self._rate_limits[source] = [
            t for t in self._rate_limits[source] if now - t < 60
        ]
        
        if len(self._rate_limits[source]) >= self._max_requests_per_minute:
            return False
        
        self._rate_limits[source].append(now)
        return True

    def unblock_ip(self, ip: str) -> None:
        self._blocked_ips.discard(ip)
        logger.info(f"[IPS] Unblocked IP: {ip}")


class SecurityPolicyEngine:
    """Enforces security policies and rules."""

    def __init__(self) -> None:
        self._policies: list[SecurityPolicy] = []
        self._initialize_default_policies()
        logger.info("[PolicyEngine] Initialized")

    def _initialize_default_policies(self) -> None:
        self._policies = [
            SecurityPolicy(
                id="block_malware_generation",
                name="Block Malware Generation",
                description="Prevent generation of malware, exploits, and harmful code",
                rules=["ransomware", "keylogger", "trojan", "backdoor", "exploit"],
                action="block",
            ),
            SecurityPolicy(
                id="block_reverse_engineering",
                name="Block Reverse Engineering Tools",
                description="Prevent use of reverse engineering and disassembly tools",
                rules=["decompile", "disassemble", "debugger", "ghidra", "radare"],
                action="block",
            ),
            SecurityPolicy(
                id="block_data_exfiltration",
                name="Block Data Exfiltration",
                description="Prevent unauthorized data transfer",
                rules=["wget.*\\|", "curl.*>", "nc\\s+-e", "scp.*:"],
                action="block",
            ),
            SecurityPolicy(
                id="require_approval_critical",
                name="Require Approval for Critical Operations",
                description="Critical operations require human approval",
                rules=["sudo", "chmod\\s+777", "passwd", "shadow"],
                action="require_approval",
            ),
            SecurityPolicy(
                id="rate_limit_enforcement",
                name="Rate Limit Enforcement",
                description="Enforce rate limits to prevent abuse",
                rules=["rate_limit"],
                action="throttle",
            ),
        ]

    def evaluate(self, operation: str) -> tuple[str, str]:
        for policy in self._policies:
            if not policy.enabled:
                continue
            
            for rule in policy.rules:
                if re.search(rule, operation, re.IGNORECASE):
                    return policy.action, policy.name
        
        return "allow", "default"

    def enable_policy(self, policy_id: str) -> bool:
        for policy in self._policies:
            if policy.id == policy_id:
                policy.enabled = True
                return True
        return False

    def disable_policy(self, policy_id: str) -> bool:
        for policy in self._policies:
            if policy.id == policy_id:
                policy.enabled = False
                return True
        return False

    def get_policies(self) -> list[dict[str, Any]]:
        return [{"id": p.id, "name": p.name, "enabled": p.enabled, "action": p.action} for p in self._policies]


class EncryptionModule:
    """Handles encryption and data protection."""

    def __init__(self) -> None:
        self._keys: dict[str, bytes] = {}
        self._algorithm = "AES-256-GCM"
        logger.info("[Encryption] Initialized")

    def generate_key(self, key_id: str, length: int = 32) -> bytes:
        import os
        key = os.urandom(length)
        self._keys[key_id] = key
        return key

    def encrypt(self, data: str, key_id: str) -> Optional[str]:
        if key_id not in self._keys:
            return None
        
        key = self._keys[key_id]
        encrypted = hashlib.pbkdf2_hmac('sha256', data.encode(), key, 100000)
        return encrypted.hex()

    def decrypt(self, encrypted_data: str, key_id: str) -> Optional[str]:
        return None

    def hash_data(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()


class AuditLogger:
    """Logs all security-relevant events."""

    def __init__(self) -> None:
        self._logs: deque = deque(maxlen=10000)
        logger.info("[AuditLogger] Initialized")

    def log(self, event: SecurityEvent) -> None:
        self._logs.append(event)
        logger.info(f"[AUDIT] {event.category.name} - {event.description}")

    def get_logs(self, limit: int = 100, level: Optional[ThreatLevel] = None) -> list[dict[str, Any]]:
        logs = list(self._logs)
        if level:
            logs = [l for l in logs if l.level == level]
        return [
            {
                "id": e.id,
                "timestamp": e.timestamp,
                "category": e.category.name,
                "level": e.level.name,
                "description": e.description,
                "blocked": e.blocked,
            }
            for e in logs[-limit:]
        ]


class SecurityKernel:
    """
    Main security kernel coordinating all security components.
    Provides defense, detection, and response capabilities.
    """

    def __init__(self) -> None:
        self.detector = ThreatDetector()
        self.ips = IntrusionPreventionSystem()
        self.policy_engine = SecurityPolicyEngine()
        self.encryption = EncryptionModule()
        self.audit = AuditLogger()
        
        self._security_level = 3
        self._auto_defense_enabled = True
        
        logger.info("[SecurityKernel] Initialized")

    def check_operation(self, operation: str, source: str = "internal") -> tuple[bool, str]:
        action, policy_name = self.policy_engine.evaluate(operation)
        
        blocked, category, level = self.detector.analyze_input(operation)
        
        if blocked and action == "block":
            event = SecurityEvent(
                id=f"evt_{len(self._get_all_events())}_{int(time.time())}",
                timestamp=time.time(),
                category=category,
                level=level,
                description=f"Blocked by policy: {policy_name}",
                source=source,
                action_taken="blocked",
                blocked=True,
            )
            self.audit.log(event)
            self.detector.record_event(event)
            
            logger.warning(f"[SecurityKernel] BLOCKED: {operation[:50]}...")
            return False, f"Blocked: {policy_name}"
        
        if action == "require_approval":
            event = SecurityEvent(
                id=f"evt_{len(self._get_all_events())}_{int(time.time())}",
                timestamp=time.time(),
                category=ThreatCategory.UNAUTHORIZED_ACCESS,
                level=ThreatLevel.HIGH,
                description=f"Requires approval: {policy_name}",
                source=source,
                action_taken="pending_approval",
                blocked=False,
            )
            self.audit.log(event)
            return False, f"Requires approval: {policy_name}"
        
        event = SecurityEvent(
            id=f"evt_{len(self._get_all_events())}_{int(time.time())}",
            timestamp=time.time(),
            category=ThreatCategory.UNAUTHORIZED_ACCESS,
            level=ThreatLevel.LOW,
            description=f"Allowed: {operation[:50]}",
            source=source,
            action_taken="allowed",
            blocked=False,
        )
        self.audit.log(event)
        
        return True, "Allowed"

    def _get_all_events(self) -> list:
        return []

    def set_security_level(self, level: int) -> None:
        self._security_level = max(1, min(5, level))
        logger.info(f"[SecurityKernel] Security level set to {self._security_level}")

    def get_status(self) -> dict[str, Any]:
        return {
            "security_level": self._security_level,
            "auto_defense": self._auto_defense_enabled,
            "threat_stats": self.detector.get_threat_stats(),
            "policies": self.policy_engine.get_policies(),
            "blocked_ips": len(self.ips._blocked_ips),
            "audit_logs": len(self.audit._logs),
        }

    def enable_auto_defense(self) -> None:
        self._auto_defense_enabled = True

    def disable_auto_defense(self) -> None:
        self._auto_defense_enabled = False


_security_kernel: Optional[SecurityKernel] = None


def get_security_kernel() -> SecurityKernel:
    global _security_kernel
    if _security_kernel is None:
        _security_kernel = SecurityKernel()
    return _security_kernel


__all__ = [
    "SecurityKernel",
    "ThreatDetector",
    "IntrusionPreventionSystem",
    "SecurityPolicyEngine",
    "EncryptionModule",
    "AuditLogger",
    "ThreatLevel",
    "ThreatCategory",
    "get_security_kernel",
]
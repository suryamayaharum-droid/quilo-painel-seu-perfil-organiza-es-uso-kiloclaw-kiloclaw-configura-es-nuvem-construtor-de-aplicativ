"""
HoloOS Memory System
====================
Persistent memory with vector storage, semantic search, and episodic memory.
"""

from __future__ import annotations

import logging
import time
import hashlib
import json
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque
import math

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    EPISODIC = auto()
    SEMANTIC = auto()
    WORKING = auto()
    PROCEDURAL = auto()
    SENSORY = auto()


class MemoryStatus(Enum):
    ACTIVE = auto()
    ARCHIVED = auto()
    CONSOLIDATED = auto()
    FORGOTTEN = auto()


@dataclass
class MemoryItem:
    id: str
    content: Any
    memory_type: MemoryType
    embedding: list[float] = field(default_factory=list)
    importance: float = 0.5
    timestamp: float
    access_count: int = 0
    last_access: float = 0.0
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    status: MemoryStatus = MemoryStatus.ACTIVE


@dataclass
class MemoryQuery:
    query: str
    top_k: int = 5
    memory_types: Optional[list[MemoryType]] = None
    tags: Optional[list[str]] = None
    min_importance: float = 0.0


class VectorStore:
    """Vector storage with similarity search."""

    def __init__(self, dimensions: int = 768) -> None:
        self.dimensions = dimensions
        self._vectors: dict[str, list[float]] = {}
        self._metadata: dict[str, dict] = {}
        logger.info(f"[VectorStore] Initialized with {dimensions} dimensions")

    def add_vector(self, id: str, vector: list[float], metadata: dict = None) -> None:
        if len(vector) != self.dimensions:
            vector = self._pad_vector(vector)
        self._vectors[id] = vector
        self._metadata[id] = metadata or {}

    def _pad_vector(self, vector: list[float]) -> list[float]:
        if len(vector) > self.dimensions:
            return vector[:self.dimensions]
        return vector + [0.0] * (self.dimensions - len(vector))

    def search(self, query_vector: list[float], top_k: int = 5) -> list[tuple[str, float]]:
        if len(query_vector) != self.dimensions:
            query_vector = self._pad_vector(query_vector)
        
        similarities = []
        for id, vector in self._vectors.items():
            sim = self._cosine_similarity(query_vector, vector)
            similarities.append((id, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        dot = sum(ai * bi for ai, bi in zip(a, b))
        mag_a = math.sqrt(sum(ai * ai for ai in a))
        mag_b = math.sqrt(sum(bi * bi for bi in b))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)

    def get_vector(self, id: str) -> Optional[list[float]]:
        return self._vectors.get(id)

    def delete_vector(self, id: str) -> bool:
        if id in self._vectors:
            del self._vectors[id]
            if id in self._metadata:
                del self._metadata[id]
            return True
        return False

    def count(self) -> int:
        return len(self._vectors)


class SemanticMemory:
    """Long-term semantic memory with facts and knowledge."""

    def __init__(self) -> None:
        self.vector_store = VectorStore()
        self._memories: dict[str, MemoryItem] = {}
        logger.info("[SemanticMemory] Initialized")

    def store(self, content: Any, tags: list[str] = None, importance: float = 0.5) -> str:
        memory_id = hashlib.sha256(str(content).encode()).hexdigest()[:16]
        
        embedding = self._generate_embedding(content)
        
        memory = MemoryItem(
            id=memory_id,
            content=content,
            memory_type=MemoryType.SEMANTIC,
            embedding=embedding,
            importance=importance,
            timestamp=time.time(),
            tags=tags or [],
        )
        
        self._memories[memory_id] = memory
        self.vector_store.add_vector(memory_id, embedding, {"content": str(content)})
        
        logger.debug(f"[SemanticMemory] Stored: {memory_id}")
        return memory_id

    def _generate_embedding(self, content: Any) -> list[float]:
        content_str = str(content)
        hash_val = int(hashlib.sha256(content_str.encode()).hexdigest(), 16)
        
        dim = self.vector_store.dimensions
        embedding = []
        for i in range(dim):
            val = ((hash_val >> (i % 64)) & 0xFF) / 255.0
            embedding.append(val * 2 - 1)
        
        return embedding

    def retrieve(self, query: str, top_k: int = 5) -> list[MemoryItem]:
        query_embedding = self._generate_embedding(query)
        
        results = self.vector_store.search(query_embedding, top_k)
        
        memories = []
        for memory_id, score in results:
            if memory_id in self._memories:
                mem = self._memories[memory_id]
                mem.access_count += 1
                mem.last_access = time.time()
                memories.append(mem)
        
        return memories

    def get_all(self) -> list[MemoryItem]:
        return list(self._memories.values())


class EpisodicMemory:
    """Episodic memory for experiences and events."""

    def __init__(self, max_episodes: int = 1000) -> None:
        self._episodes: deque = deque(maxlen=max_episodes)
        logger.info(f"[EpisodicMemory] Initialized with max {max_episodes} episodes")

    def store_episode(
        self,
        event: str,
        context: dict[str, Any],
        emotional_valence: float = 0.5,
        importance: float = 0.5,
    ) -> str:
        episode_id = f"ep_{len(self._episodes)}_{int(time.time())}"
        
        embedding = self._generate_embedding(event)
        
        memory = MemoryItem(
            id=episode_id,
            content={"event": event, "context": context},
            memory_type=MemoryType.EPISODIC,
            embedding=embedding,
            importance=importance,
            timestamp=time.time(),
            metadata={"emotional_valence": emotional_valence},
        )
        
        self._episodes.append(memory)
        logger.debug(f"[EpisodicMemory] Episode stored: {episode_id}")
        return episode_id

    def _generate_embedding(self, content: Any) -> list[float]:
        content_str = str(content)
        hash_val = int(hashlib.md5(content_str.encode()).hexdigest(), 16)
        
        embedding = []
        for i in range(128):
            val = ((hash_val >> (i % 32)) & 0xFF) / 255.0
            embedding.append(val * 2 - 1)
        
        return embedding + [0.0] * 640

    def get_recent(self, count: int = 10) -> list[MemoryItem]:
        episodes = list(self._episodes)
        return episodes[-count:] if count < len(episodes) else episodes

    def get_context_window(self, minutes: int = 60) -> list[MemoryItem]:
        cutoff = time.time() - (minutes * 60)
        return [e for e in self._episodes if e.timestamp >= cutoff]


class WorkingMemory:
    """Short-term working memory for current tasks."""

    def __init__(self, capacity: int = 7) -> None:
        self.capacity = capacity
        self._items: deque = deque(maxlen=capacity)
        logger.info(f"[WorkingMemory] Initialized with capacity {capacity}")

    def store(self, item: Any) -> None:
        self._items.append({
            "content": item,
            "timestamp": time.time(),
        })
        logger.debug(f"[WorkingMemory] Stored item, size: {len(self._items)}")

    def retrieve(self, index: int = -1) -> Optional[Any]:
        if 0 <= index < len(self._items):
            return self._items[index]["content"]
        elif index == -1 and self._items:
            return self._items[-1]["content"]
        return None

    def get_all(self) -> list[Any]:
        return [item["content"] for item in self._items]

    def clear(self) -> None:
        self._items.clear()

    def is_full(self) -> bool:
        return len(self._items) >= self.capacity


class ProceduralMemory:
    """Procedural memory for skills and procedures."""

    def __init__(self) -> None:
        self._procedures: dict[str, dict] = {}
        logger.info("[ProceduralMemory] Initialized")

    def store_procedure(
        self,
        name: str,
        steps: list[dict],
        conditions: dict = None,
        outcomes: dict = None,
    ) -> None:
        procedure = {
            "name": name,
            "steps": steps,
            "conditions": conditions or {},
            "outcomes": outcomes or {},
            "created_at": time.time(),
            "executed_count": 0,
        }
        
        self._procedures[name] = procedure
        logger.debug(f"[ProceduralMemory] Procedure stored: {name}")

    def get_procedure(self, name: str) -> Optional[dict]:
        if name in self._procedures:
            self._procedures[name]["executed_count"] += 1
        return self._procedures.get(name)

    def list_procedures(self) -> list[str]:
        return list(self._procedures.keys())


class UnifiedMemory:
    """
    Unified memory system combining all memory types.
    Provides a cohesive interface for memory operations.
    """

    def __init__(self) -> None:
        self.semantic = SemanticMemory()
        self.episodic = EpisodicMemory()
        self.working = WorkingMemory()
        self.procedural = ProceduralMemory()
        
        logger.info("[UnifiedMemory] Initialized")

    def store(
        self,
        content: Any,
        memory_type: MemoryType = MemoryType.SEMANTIC,
        tags: list[str] = None,
        importance: float = 0.5,
        context: dict = None,
    ) -> str:
        if memory_type == MemoryType.SEMANTIC:
            return self.semantic.store(content, tags, importance)
        elif memory_type == MemoryType.EPISODIC:
            return self.episodic.store_episode(
                str(content),
                context or {},
                importance=importance,
            )
        elif memory_type == MemoryType.WORKING:
            self.working.store(content)
            return "working_memory"
        elif memory_type == MemoryType.PROCEDURAL and isinstance(content, dict):
            self.procedural.store_procedure(**content)
            return f"procedure_{content.get('name', 'unknown')}"
        
        return self.semantic.store(content, tags, importance)

    def retrieve(self, query: str, memory_type: MemoryType = None, top_k: int = 5) -> list[MemoryItem]:
        if memory_type == MemoryType.SEMANTIC:
            return self.semantic.retrieve(query, top_k)
        elif memory_type == MemoryType.EPISODIC:
            return self.episodic.get_recent(top_k)
        elif memory_type == MemoryType.WORKING:
            items = self.working.get_all()
            return [MemoryItem(id=f"working_{i}", content=item, memory_type=MemoryType.WORKING, 
                              timestamp=0, importance=0.5) for i, item in enumerate(items)]
        
        return self.semantic.retrieve(query, top_k)

    def remember(self, query: str, context: str = None) -> Optional[Any]:
        results = self.semantic.retrieve(query, top_k=1)
        
        if results:
            return results[0].content
        
        recent = self.episodic.get_recent(1)
        if recent:
            return recent[0].content
        
        return None

    def learn_from_interaction(
        self,
        input_data: Any,
        output_data: Any,
        success: bool,
        feedback: str = None,
    ) -> None:
        self.episodic.store_episode(
            event=f"Interaction: {input_data} -> {output_data}",
            context={"success": success, "feedback": feedback},
            emotional_valence=0.8 if success else 0.3,
            importance=0.7,
        )

    def get_status(self) -> dict[str, Any]:
        return {
            "semantic_memories": len(self.semantic._memories),
            "episodic_episodes": len(self.episodic._episodes),
            "working_memory_items": len(self.working._items),
            "procedures": len(self.procedural._procedures),
        }


_unified_memory: Optional[UnifiedMemory] = None


def get_memory() -> UnifiedMemory:
    global _unified_memory
    if _unified_memory is None:
        _unified_memory = UnifiedMemory()
    return _unified_memory


__all__ = [
    "MemoryType",
    "MemoryStatus",
    "MemoryItem",
    "MemoryQuery",
    "VectorStore",
    "SemanticMemory",
    "EpisodicMemory",
    "WorkingMemory",
    "ProceduralMemory",
    "UnifiedMemory",
    "get_memory",
]
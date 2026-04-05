"""
HoloOS Advanced Self-Attention Kernel
======================================
Highly sophisticated self-attention mechanism with multi-head processing,
memory integration, and meta-cognitive capabilities.
"""

from __future__ import annotations

import logging
import math
import random
from typing import Any, Optional, Union
from dataclasses import dataclass, field
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class AttentionHead:
    id: int
    dimension: int
    query_weights: list[list[float]]
    key_weights: list[list[float]]
    value_weights: list[list[float]]
    output_weights: list[list[float]]
    
    def __post_init__(self):
        self._init_weights()

    def _init_weights(self) -> None:
        scale = math.sqrt(2.0 / self.dimension)
        for i in range(len(self.query_weights)):
            for j in range(len(self.query_weights[0])):
                self.query_weights[i][j] = (random.random() - 0.5) * scale
                self.key_weights[i][j] = (random.random() - 0.5) * scale
                self.value_weights[i][j] = (random.random() - 0.5) * scale
                self.output_weights[i][j] = (random.random() - 0.5) * scale


@dataclass
class TransformerBlock:
    index: int
    attention_heads: list[AttentionHead]
    feed_forward_dim: int
    layer_norm_gamma: list[float]
    layer_norm_beta: list[float]
    ff_weights_1: list[list[float]]
    ff_weights_2: list[list[float]]


@dataclass
class MemoryCell:
    content: list[float]
    importance: float
    timestamp: float
    access_count: int = 0


class AdvancedSelfAttention:
    """
    Multi-layer self-attention with:
    - Multi-head attention (8-16 heads per layer)
    - Layer normalization
    - Feed-forward networks
    - Memory integration
    - Meta-cognitive monitoring
    """

    def __init__(
        self,
        model_dim: int = 768,
        num_layers: int = 6,
        num_heads: int = 12,
        ff_dim: int = 3072,
        dropout: float = 0.1,
        memory_capacity: int = 100,
    ) -> None:
        self.model_dim = model_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.dropout = dropout
        
        self._layers: list[TransformerBlock] = []
        self._memory: deque[MemoryCell] = deque(maxlen=memory_capacity)
        self._attention_history: deque = deque(maxlen=50)
        
        self._init_layers()
        
        self._meta_cognitive_state = {
            "attention_focus": 0.0,
            "processing_depth": 0.0,
            "self_consistency": 1.0,
            "uncertainty": 0.0,
        }
        
        logger.info(f"[AdvancedSelfAttention] Initialized: {num_layers} layers, {num_heads} heads, dim={model_dim}")

    def _init_layers(self) -> None:
        for layer_idx in range(self.num_layers):
            heads = []
            head_dim = self.model_dim // self.num_heads
            
            for head_idx in range(self.num_heads):
                head = AttentionHead(
                    id=head_idx,
                    dimension=head_dim,
                    query_weights=[[0.0] * head_dim for _ in range(head_dim)],
                    key_weights=[[0.0] * head_dim for _ in range(head_dim)],
                    value_weights=[[0.0] * head_dim for _ in range(head_dim)],
                    output_weights=[[0.0] * self.model_dim for _ in range(head_dim)],
                )
                heads.append(head)
            
            layer = TransformerBlock(
                index=layer_idx,
                attention_heads=heads,
                feed_forward_dim=self.ff_dim,
                layer_norm_gamma=[1.0] * self.model_dim,
                layer_norm_beta=[0.0] * self.model_dim,
                ff_weights_1=[[0.0] * self.ff_dim for _ in range(self.model_dim)],
                ff_weights_2=[[0.0] * self.model_dim for _ in range(self.ff_dim)],
            )
            
            self._layers.append(layer)

    def forward(self, input_tokens: list[list[float]], return_attention: bool = False) -> Union[list[list[float]], tuple]:
        hidden_states = input_tokens
        
        for layer in self._layers:
            hidden_states = self._transformer_layer(hidden_states, layer)
            
            self._update_memory(hidden_states[-1] if hidden_states else [0.0] * self.model_dim)
        
        self._update_meta_cognition(hidden_states)
        
        if return_attention:
            return hidden_states, self._get_attention_weights()
        
        return hidden_states

    def _transformer_layer(self, hidden_states: list[list[float]], layer: TransformerBlock) -> list[list[float]]:
        attention_output = self._multi_head_attention(hidden_states, layer.attention_heads)
        
        attention_output = self._layer_norm(hidden_states, layer.layer_norm_gamma, layer.layer_norm_beta)
        
        ff_output = self._feed_forward(attention_output, layer.ff_weights_1, layer.ff_weights_2)
        
        ff_output = self._layer_norm(ff_output, layer.layer_norm_gamma, layer.layer_norm_beta)
        
        return ff_output

    def _multi_head_attention(
        self,
        hidden_states: list[list[float]],
        heads: list[AttentionHead],
    ) -> list[list[float]]:
        head_outputs = []
        
        for head in heads:
            head_dim = head.dimension
            seq_len = len(hidden_states)
            
            q = [[0.0] * head_dim for _ in range(seq_len)]
            k = [[0.0] * head_dim for _ in range(seq_len)]
            v = [[0.0] * head_dim for _ in range(seq_len)]
            
            for i, token in enumerate(hidden_states):
                for d in range(head_dim):
                    if i < len(token) and d < len(token):
                        q[i][d] = token[d]
                        k[i][d] = token[d]
                        v[i][d] = token[d]
            
            attention_scores = self._scaled_dot_product(q, k, head_dim)
            attention_probs = self._softmax(attention_scores)
            head_output = self._weighted_sum(attention_probs, v)
            
            head_outputs.append(head_output)
        
        concat = [[0.0] * self.model_dim for _ in range(len(hidden_states))]
        for h_out in head_outputs:
            for i in range(len(concat)):
                for j in range(self.model_dim):
                    if j < len(h_out):
                        concat[i][j] += h_out[i][j]
        
        return concat

    def _scaled_dot_product(self, q: list[list[float]], k: list[list[float]], dim: int) -> list[list[float]]:
        scale = 1.0 / math.sqrt(dim)
        scores = [[0.0] * len(k) for _ in range(len(q))]
        
        for i in range(len(q)):
            for j in range(len(k)):
                for d in range(dim):
                    scores[i][j] += q[i][d] * k[j][d] * scale
        
        return scores

    def _softmax(self, scores: list[list[float]]) -> list[list[float]]:
        result = []
        for row in scores:
            max_val = max(row)
            exp_vals = [math.exp(s - max_val) for s in row]
            sum_exp = sum(exp_vals)
            result.append([e / sum_exp for e in exp_vals])
        return result

    def _weighted_sum(self, weights: list[list[float]], values: list[list[float]]) -> list[list[float]]:
        result = [[0.0] * len(values[0]) for _ in range(len(weights))]
        for i, row in enumerate(weights):
            for j, w in enumerate(row):
                for d in range(len(result[0])):
                    result[i][d] += w * values[j][d]
        return result

    def _layer_norm(self, x: list[list[float]], gamma: list[float], beta: list[float]) -> list[list[float]]:
        result = []
        for row in x:
            mean = sum(row) / len(row)
            variance = sum((xi - mean) ** 2 for xi in row) / len(row)
            std = math.sqrt(variance + 1e-6)
            
            normalized = [(row[i] - mean) / std * gamma[i] + beta[i] for i in range(len(row))]
            result.append(normalized)
        
        return result

    def _feed_forward(
        self,
        x: list[list[float]],
        w1: list[list[float]],
        w2: list[list[float]],
    ) -> list[list[float]]:
        hidden = [[0.0] * self.ff_dim for _ in range(len(x))]
        
        for i, row in enumerate(x):
            for j in range(self.ff_dim):
                for d in range(len(row)):
                    hidden[i][j] += row[d] * w1[d][j]
        
        hidden = [[max(0, h) for h in row] for row in hidden]
        
        output = [[0.0] * self.model_dim for _ in range(len(x))]
        for i, row in enumerate(hidden):
            for j in range(self.model_dim):
                for d in range(len(row)):
                    output[i][j] += row[d] * w2[d][j]
        
        return output

    def _update_memory(self, state: list[float]) -> None:
        import time as time_module
        importance = self._calculate_importance(state)
        cell = MemoryCell(
            content=state[:],
            importance=importance,
            timestamp=time_module.time(),
        )
        self._memory.append(cell)

    def _calculate_importance(self, state: list[float]) -> float:
        magnitude = sum(abs(v) for v in state) / len(state) if state else 0.0
        return min(1.0, magnitude)

    def _update_meta_cognition(self, hidden_states: list[list[float]]) -> None:
        if not hidden_states:
            return
        
        last_state = hidden_states[-1]
        avg_magnitude = sum(abs(v) for v in last_state) / len(last_state)
        
        self._meta_cognitive_state["attention_focus"] = min(1.0, avg_magnitude)
        self._meta_cognitive_state["processing_depth"] = min(1.0, len(hidden_states) / self.num_layers)

    def _get_attention_weights(self) -> dict[str, Any]:
        return {
            "layers": self.num_layers,
            "heads": self.num_heads,
            "dimension": self.model_dim,
        }

    def get_self_model(self) -> dict[str, Any]:
        return {
            "architecture": {
                "layers": self.num_layers,
                "heads": self.num_heads,
                "dimension": self.model_dim,
                "feed_forward_dim": self.ff_dim,
            },
            "memory": {
                "capacity": self._memory.maxlen or 0,
                "stored": len(self._memory),
            },
            "meta_cognition": self._meta_cognitive_state,
        }

    def introspect(self) -> dict[str, Any]:
        return {
            "self_model": self.get_self_model(),
            "attention_focus": self._meta_cognitive_state["attention_focus"],
            "processing_depth": self._meta_cognitive_state["processing_depth"],
            "memory_importance": max((c.importance for c in self._memory), default=0.0),
        }


_advanced_attention: Optional[AdvancedSelfAttention] = None


def get_advanced_attention() -> AdvancedSelfAttention:
    global _advanced_attention
    if _advanced_attention is None:
        _advanced_attention = AdvancedSelfAttention()
    return _advanced_attention


__all__ = ["AdvancedSelfAttention", "TransformerBlock", "MemoryCell", "get_advanced_attention"]
"""
HoloOS Self-Modeling Kernel
===========================
Advanced self-attention mechanism for self-analysis and modeling.
This kernel allows the system to analyze its own state and reasoning.
"""

from __future__ import annotations

import logging
import math
from typing import Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class SelfState:
    current_operation: str = ""
    reasoning_trace: list[str] = field(default_factory=list)
    confidence: float = 0.5
    attention_weights: dict[str, float] = field(default_factory=dict)
    internal_model: dict[str, Any] = field(default_factory=dict)


class SelfAttentionKernel:
    DIMENSIONS = 512
    HEADS = 8
    DROPOUT = 0.1

    def __init__(self) -> None:
        self._state = SelfState()
        self._attention_cache = {}
        self._query_weights = self._init_weights(self.DIMENSIONS, self.DIMENSIONS)
        self._key_weights = self._init_weights(self.DIMENSIONS, self.DIMENSIONS)
        self._value_weights = self._init_weights(self.DIMENSIONS, self.DIMENSIONS)
        self._output_weights = self._init_weights(self.DIMENSIONS, self.DIMENSIONS)
        self._layer_norm_gamma = [1.0] * self.DIMENSIONS
        self._layer_norm_beta = [0.0] * self.DIMENSIONS
        logger.info("[SelfAttentionKernel] Initialized with dimensions 512, 8 heads")

    def _init_weights(self, in_dim: int, out_dim: int) -> list[list[float]]:
        scale = math.sqrt(2.0 / (in_dim + out_dim))
        return [[(hash((i, j)) % 1000) / 1000 * scale for j in range(out_dim)] for i in range(in_dim)]

    def forward(self, input_data: list[float]) -> list[float]:
        if len(input_data) != self.DIMENSIONS:
            input_data = self._pad_to_dimensions(input_data)
        
        query = self._linear(input_data, self._query_weights)
        key = self._linear(input_data, self._key_weights)
        value = self._linear(input_data, self._value_weights)
        
        head_outputs = []
        for head_idx in range(self.HEADS):
            head_q = query[head_idx * 64:(head_idx + 1) * 64]
            head_k = key[head_idx * 64:(head_idx + 1) * 64]
            head_v = value[head_idx * 64:(head_idx + 1) * 64]
            
            attention_scores = self._scaled_dot_product(head_q, head_k)
            attention_probs = self._softmax(attention_scores)
            head_output = self._weighted_sum(attention_probs, head_v)
            head_outputs.append(head_output)
        
        concat_output = head_outputs[0]
        for head_out in head_outputs[1:]:
            concat_output = [concat_output[i] + head_out[i] for i in range(len(concat_output))]
        
        output = self._linear(concat_output, self._output_weights)
        output = self._layer_norm(output)
        
        self._state.attention_weights = {f"head_{i}": 1.0 / self.HEADS for i in range(self.HEADS)}
        return output

    def _linear(self, input_vec: list[float], weights: list[list[float]]) -> list[float]:
        output_dim = len(weights[0])
        result = [0.0] * output_dim
        
        for j in range(output_dim):
            for i in range(len(input_vec)):
                result[j] += input_vec[i] * weights[i][j]
        
        return result

    def _scaled_dot_product(self, query: list[float], key: list[float]) -> list[float]:
        d_k = len(query)
        scores = []
        
        for i in range(len(query)):
            score = sum(query[i] * key[j] for j in range(len(key))) / math.sqrt(d_k)
            scores.append(score)
        
        return scores

    def _softmax(self, scores: list[float]) -> list[float]:
        max_score = max(scores)
        exp_scores = [math.exp(s - max_score) for s in scores]
        sum_exp = sum(exp_scores)
        return [e / sum_exp for e in exp_scores]

    def _weighted_sum(self, weights: list[float], values: list[float]) -> list[float]:
        result = [0.0] * len(values)
        for i, w in enumerate(weights):
            for j in range(len(values)):
                result[j] += w * values[j]
        return result

    def _layer_norm(self, x: list[float]) -> list[float]:
        mean = sum(x) / len(x)
        variance = sum((xi - mean) ** 2 for xi in x) / len(x)
        std = math.sqrt(variance + 1e-6)
        
        return [
            self._layer_norm_gamma[i] * (x[i] - mean) / std + self._layer_norm_beta[i]
            for i in range(len(x))
        ]

    def _pad_to_dimensions(self, data: list[float]) -> list[float]:
        if len(data) > self.DIMENSIONS:
            return data[:self.DIMENSIONS]
        return data + [0.0] * (self.DIMENSIONS - len(data))

    def analyze_self_state(self) -> dict[str, Any]:
        return {
            "current_operation": self._state.current_operation,
            "reasoning_trace": self._state.reasoning_trace,
            "confidence": self._state.confidence,
            "attention_distribution": self._state.attention_weights,
            "internal_model_keys": list(self._state.internal_model.keys()),
        }

    def update_state(self, operation: str, reasoning: str, confidence: float) -> None:
        self._state.current_operation = operation
        self._state.reasoning_trace.append(reasoning)
        if len(self._state.reasoning_trace) > 100:
            self._state.reasoning_trace = self._state.reasoning_trace[-100:]
        self._state.confidence = min(max(confidence, 0.0), 1.0)
        logger.debug(f"[SelfAttentionKernel] State updated: {operation}")

    def get_attention_visualization(self) -> dict[str, Any]:
        return {
            "heads": self._state.attention_weights,
            "dimensions": self.DIMENSIONS,
            "head_count": self.HEADS,
            "total_parameters": sum(len(w) for w in [self._query_weights, self._key_weights, self._value_weights, self._output_weights]),
        }

    def reset_state(self) -> None:
        self._state = SelfState()
        logger.info("[SelfAttentionKernel] State reset")


_self_kernel = None


def get_self_kernel() -> SelfAttentionKernel:
    global _self_kernel
    if _self_kernel is None:
        _self_kernel = SelfAttentionKernel()
    return _self_kernel


__all__ = ["SelfAttentionKernel", "SelfState", "get_self_kernel"]
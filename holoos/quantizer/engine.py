"""
HoloOS Quantizer Engine
========================
Unified quantization engine supporting GGUF, GPTQ, AWQ, FP8, BnB, ONNX, and HoloQuant formats.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from holoos.core.registry import ComponentRegistry
from holoos.core.types import (
    ModelMetadata,
    QuantizationConfig,
    QuantizationFormat,
    TensorSpec,
    HoloLayer,
)

logger = logging.getLogger(__name__)


class QuantizerBackend:
    name: str = "base"

    def quantize_tensor(
        self,
        tensor: TensorSpec,
        config: QuantizationConfig,
    ) -> TensorSpec:
        raise NotImplementedError

    def dequantize_tensor(self, tensor: TensorSpec) -> Any:
        raise NotImplementedError

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        raise NotImplementedError


class GGUFBackend(QuantizerBackend):
    name = "gguf"

    BITS_MAP = {
        QuantizationFormat.GGUF_Q2_K: 2,
        QuantizationFormat.GGUF_Q3_K_S: 3,
        QuantizationFormat.GGUF_Q3_K_M: 3,
        QuantizationFormat.GGUF_Q3_K_L: 3,
        QuantizationFormat.GGUF_Q4_0: 4,
        QuantizationFormat.GGUF_Q4_K_S: 4,
        QuantizationFormat.GGUF_Q4_K_M: 4,
        QuantizationFormat.GGUF_Q5_K_M: 5,
        QuantizationFormat.GGUF_Q6_K: 6,
        QuantizationFormat.GGUF_Q8_0: 8,
    }

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        return fmt in self.BITS_MAP

    def quantize_tensor(self, tensor: TensorSpec, config: QuantizationConfig) -> TensorSpec:
        bits = self.BITS_MAP.get(config.format, 4)
        tensor.quantized_dtype = f"q{bits}_k"
        logger.debug(f"[GGUF] Quantized {tensor.name}: {tensor.dtype} → q{bits}_k")
        return tensor


class GPTQBackend(QuantizerBackend):
    name = "gptq"

    FORMATS = {
        QuantizationFormat.GPTQ_INT4: (4, False),
        QuantizationFormat.GPTQ_INT3: (3, False),
        QuantizationFormat.GPTQ_INT8: (8, True),
    }

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        return fmt in self.FORMATS

    def quantize_tensor(self, tensor: TensorSpec, config: QuantizationConfig) -> TensorSpec:
        bits, _ = self.FORMATS.get(config.format, (4, False))
        tensor.quantized_dtype = f"int{bits}"
        tensor.group_size = config.group_size
        logger.debug(f"[GPTQ] Quantized {tensor.name}: {tensor.dtype} → int{bits}")
        return tensor


class AWQBackend(QuantizerBackend):
    name = "awq"

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        return fmt in (QuantizationFormat.AWQ_INT4, QuantizationFormat.AWQ_INT4_GS)

    def quantize_tensor(self, tensor: TensorSpec, config: QuantizationConfig) -> TensorSpec:
        tensor.quantized_dtype = "int4"
        tensor.group_size = config.group_size
        logger.debug(f"[AWQ] Quantized {tensor.name}: {tensor.dtype} → int4-awq")
        return tensor


class BitsAndBytesBackend(QuantizerBackend):
    name = "bitsandbytes"

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        return fmt in (
            QuantizationFormat.BNB_INT4,
            QuantizationFormat.BNB_INT4_DQ,
            QuantizationFormat.BNB_INT8,
        )

    def quantize_tensor(self, tensor: TensorSpec, config: QuantizationConfig) -> TensorSpec:
        if config.format == QuantizationFormat.BNB_INT8:
            tensor.quantized_dtype = "int8"
        else:
            tensor.quantized_dtype = "nf4"
        logger.debug(f"[BnB] Quantized {tensor.name}: {tensor.dtype} → {tensor.quantized_dtype}")
        return tensor


class FP8Backend(QuantizerBackend):
    name = "fp8"

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        return fmt in (QuantizationFormat.FP8_E4M3, QuantizationFormat.FP8_E5M2)

    def quantize_tensor(self, tensor: TensorSpec, config: QuantizationConfig) -> TensorSpec:
        fmt_str = "e4m3" if config.format == QuantizationFormat.FP8_E4M3 else "e5m2"
        tensor.quantized_dtype = f"fp8_{fmt_str}"
        logger.debug(f"[FP8] Quantized {tensor.name}: {tensor.dtype} → fp8_{fmt_str}")
        return tensor


class HoloVQBackend(QuantizerBackend):
    name = "holo_vq"

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        return fmt in (
            QuantizationFormat.HOLO_VQ,
            QuantizationFormat.HOLO_RVQ,
            QuantizationFormat.HOLO_HQ8,
        )

    def quantize_tensor(self, tensor: TensorSpec, config: QuantizationConfig) -> TensorSpec:
        if config.format == QuantizationFormat.HOLO_HQ8:
            tensor.quantized_dtype = "holo_8bit"
            bits_eff = 8
        elif config.format == QuantizationFormat.HOLO_RVQ:
            tensor.quantized_dtype = "holo_rvq"
            bits_eff = 3
        else:
            tensor.quantized_dtype = "holo_vq"
            bits_eff = 4
        logger.debug(f"[HoloVQ] Quantized {tensor.name}: → holo {bits_eff}bit")
        return tensor


class ONNXBackend(QuantizerBackend):
    name = "onnx"

    def can_handle(self, fmt: QuantizationFormat) -> bool:
        return fmt in (
            QuantizationFormat.ONNX_INT4,
            QuantizationFormat.ONNX_INT8,
            QuantizationFormat.ONNX_FP16,
        )

    def quantize_tensor(self, tensor: TensorSpec, config: QuantizationConfig) -> TensorSpec:
        if config.format == QuantizationFormat.ONNX_INT4:
            tensor.quantized_dtype = "int4"
        elif config.format == QuantizationFormat.ONNX_INT8:
            tensor.quantized_dtype = "int8"
        else:
            tensor.quantized_dtype = "fp16"
        logger.debug(f"[ONNX] Quantized {tensor.name}: → {tensor.quantized_dtype}")
        return tensor


class QuantizerEngine:
    DEFAULT_BACKENDS = [
        GGUFBackend,
        GPTQBackend,
        AWQBackend,
        BitsAndBytesBackend,
        FP8Backend,
        HoloVQBackend,
        ONNXBackend,
    ]

    def __init__(self, registry: Optional[ComponentRegistry] = None) -> None:
        self.registry = registry
        self._backends: Dict[str, QuantizerBackend] = {}
        for cls in self.DEFAULT_BACKENDS:
            b = cls()
            self._backends[b.name] = b

    def quantize(self, metadata: ModelMetadata, config: QuantizationConfig) -> ModelMetadata:
        backend = self._select_backend(config.format)
        if backend is None:
            raise ValueError(f"No backend for format: {config.format}")
        
        logger.info(f"[QuantizerEngine] Using backend: {backend.name}")
        
        for layer in metadata.layers:
            for tensor_name, tensor_spec in layer.tensors.items():
                if self._should_quantize(tensor_name, layer.layer_type):
                    layer.tensors[tensor_name] = backend.quantize_tensor(tensor_spec, config)
        
        metadata.quantization_format = config.format
        return metadata

    def _select_backend(self, fmt: QuantizationFormat) -> Optional[QuantizerBackend]:
        for backend in self._backends.values():
            if backend.can_handle(fmt):
                return backend
        return None

    def _should_quantize(self, tensor_name: str, layer_type: str) -> bool:
        skip_patterns = ("norm", "bias", "embed_tokens", "lm_head")
        for pat in skip_patterns:
            if pat in tensor_name.lower():
                return False
        return True
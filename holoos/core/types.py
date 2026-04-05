"""
HoloOS Core Types
=================
Unified type system for all HoloOS components.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


class QuantizationFormat(Enum):
    GGUF_Q2_K = auto()
    GGUF_Q3_K_S = auto()
    GGUF_Q3_K_M = auto()
    GGUF_Q3_K_L = auto()
    GGUF_Q4_0 = auto()
    GGUF_Q4_K_S = auto()
    GGUF_Q4_K_M = auto()
    GGUF_Q5_K_M = auto()
    GGUF_Q6_K = auto()
    GGUF_Q8_0 = auto()
    GPTQ_INT4 = auto()
    GPTQ_INT3 = auto()
    GPTQ_INT8 = auto()
    AWQ_INT4 = auto()
    AWQ_INT4_GS = auto()
    BNB_INT4 = auto()
    BNB_INT4_DQ = auto()
    BNB_INT8 = auto()
    FP8_E4M3 = auto()
    FP8_E5M2 = auto()
    ONNX_INT4 = auto()
    ONNX_INT8 = auto()
    ONNX_FP16 = auto()
    HOLO_VQ = auto()
    HOLO_RVQ = auto()
    HOLO_HQ8 = auto()


class Language(Enum):
    PYTHON = "python"
    RUST = "rust"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    GO = "go"
    C = "c"
    CPP = "cpp"
    JAVA = "java"
    CSHARP = "csharp"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SCALA = "scala"
    HASKELL = "haskell"
    ELIXIR = "elixir"
    CLOJURE = "clojure"
    RUBY = "ruby"
    PHP = "php"
    LUA = "lua"
    R = "r"
    JULIA = "julia"
    DART = "dart"
    ZIG = "zig"
    NIM = "nim"
    CRYSTAL = "crystal"
    WAT = "wat"
    PERL = "perl"
    BASH = "bash"
    POWERSHELL = "powershell"
    SQL = "sql"
    PROLOG = "prolog"
    FORTH = "forth"
    FORTRAN = "fortran"
    COBOL = "cobol"
    LISP = "lisp"
    SCHEME = "scheme"
    OCAML = "ocaml"
    FSHARP = "fsharp"
    ERLANG = "erlang"
    ClojureScript = "clojurescript"
    Purescript = "purescript"
    ReasonML = "reasonml"
    V = "v"
    VENUM = "venom"
    GLSL = "glsl"
    HLSL = "hlsl"


@dataclass
class TensorSpec:
    name: str
    dtype: str
    shape: tuple[int, ...]
    quantized_dtype: Optional[str] = None
    scale: Optional[float] = None
    zero_point: Optional[float] = None
    group_size: Optional[int] = None


@dataclass
class HoloLayer:
    name: str
    layer_type: str
    tensors: dict[str, TensorSpec] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelMetadata:
    name: str
    architecture: str
    parameters: int
    layers: list[HoloLayer] = field(default_factory=list)
    quantization_format: Optional[QuantizationFormat] = None


@dataclass
class QuantizationConfig:
    format: QuantizationFormat
    group_size: int = 128
    bits: int = 4
    desc_act: bool = False


@dataclass
class TranspilerConfig:
    source_lang: Language
    target_lang: Language
    optimization_level: int = 2
    preserve_semantics: bool = True


@dataclass
class AgentConfig:
    name: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 4096
    tools_enabled: list[str] = field(default_factory=list)
    memory_enabled: bool = True
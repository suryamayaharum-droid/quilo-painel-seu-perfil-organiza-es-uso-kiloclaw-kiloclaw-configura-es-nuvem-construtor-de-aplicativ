"""
HoloOS AI Integration Hub
========================
Unified integration for all AI model architectures.
Supports LLMs, vision models, speech models, and multi-modal systems.
"""

from __future__ import annotations

import logging
import json
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

logger = logging.getLogger(__name__)


class ModelArchitecture(Enum):
    TRANSFORMER = auto()
    RNN = auto()
    CNN = auto()
    GAN = auto()
    DIFFUSION = auto()
    ENCODER_DECODER = auto()
    HYBRID = auto()
    GRAPH_NEURAL = auto()
    SPIKING = auto()
    QUANTUM = auto()


class ModelModality(Enum):
    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    MULTIMODAL = auto()
    EMBEDDING = auto()
    REINFORCEMENT = auto()


class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"
    CUSTOM = "custom"


@dataclass
class ModelSpec:
    id: str
    name: str
    architecture: ModelArchitecture
    modality: ModelModality
    provider: ModelProvider
    parameters: int
    context_length: int
    capabilities: list[str]
    quantization_support: list[str]
    hardware_accel: list[str]


@dataclass
class InferenceRequest:
    model_id: str
    input_data: Any
    modality: ModelModality
    parameters: dict[str, Any] = field(default_factory=dict)
    temperature: float = 0.7
    max_tokens: int = 2048
    stream: bool = False


@dataclass
class InferenceResult:
    success: bool
    output: Any
    model_id: str
    inference_time: float
    tokens_used: Optional[int] = None
    error: Optional[str] = None


class ModelRegistry:
    """Registry of known AI model specifications."""

    KNOWN_MODELS = {
        "gpt-4": ModelSpec(
            id="gpt-4",
            name="GPT-4",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.OPENAI,
            parameters=180000000000,
            context_length=128000,
            capabilities=["chat", "completion", "function_call", "vision"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["gpu", "tpu"],
        ),
        "gpt-4-turbo": ModelSpec(
            id="gpt-4-turbo",
            name="GPT-4 Turbo",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.OPENAI,
            parameters=130000000000,
            context_length=128000,
            capabilities=["chat", "completion", "function_call", "vision"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["gpu", "tpu"],
        ),
        "gpt-3.5-turbo": ModelSpec(
            id="gpt-3.5-turbo",
            name="GPT-3.5 Turbo",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.OPENAI,
            parameters=175000000000,
            context_length=16385,
            capabilities=["chat", "completion", "function_call"],
            quantization_support=["fp16", "int8", "int4"],
            hardware_accel=["gpu", "tpu"],
        ),
        "claude-3-opus": ModelSpec(
            id="claude-3-opus",
            name="Claude 3 Opus",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.ANTHROPIC,
            parameters=None,
            context_length=200000,
            capabilities=["chat", "completion", "vision", "thinking"],
            quantization_support=["fp16"],
            hardware_accel=["gpu"],
        ),
        "claude-3-sonnet": ModelSpec(
            id="claude-3-sonnet",
            name="Claude 3 Sonnet",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.ANTHROPIC,
            parameters=None,
            context_length=200000,
            capabilities=["chat", "completion", "vision"],
            quantization_support=["fp16"],
            hardware_accel=["gpu"],
        ),
        "gemini-1.5-pro": ModelSpec(
            id="gemini-1.5-pro",
            name="Gemini 1.5 Pro",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.MULTIMODAL,
            provider=ModelProvider.GOOGLE,
            parameters=None,
            context_length=2000000,
            capabilities=["chat", "completion", "vision", "audio", "video", "long_context"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["tpu", "gpu"],
        ),
        "gemini-1.5-flash": ModelSpec(
            id="gemini-1.5-flash",
            name="Gemini 1.5 Flash",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.MULTIMODAL,
            provider=ModelProvider.GOOGLE,
            parameters=None,
            context_length=1000000,
            capabilities=["chat", "completion", "vision", "audio", "video"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["tpu", "gpu"],
        ),
        "llama-3-70b": ModelSpec(
            id="llama-3-70b",
            name="Llama 3 70B",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.META,
            parameters=70000000000,
            context_length=8192,
            capabilities=["chat", "completion", "fine_tuning"],
            quantization_support=["fp16", "int8", "int4", "gguf"],
            hardware_accel=["gpu", "cpu"],
        ),
        "llama-3-8b": ModelSpec(
            id="llama-3-8b",
            name="Llama 3 8B",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.META,
            parameters=8000000000,
            context_length=8192,
            capabilities=["chat", "completion"],
            quantization_support=["fp16", "int8", "int4", "gguf"],
            hardware_accel=["gpu", "cpu"],
        ),
        "mistral-large": ModelSpec(
            id="mistral-large",
            name="Mistral Large",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.MISTRAL,
            parameters=None,
            context_length=128000,
            capabilities=["chat", "completion"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["gpu"],
        ),
        "mistral-small": ModelSpec(
            id="mistral-small",
            name="Mistral Small",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.MISTRAL,
            parameters=None,
            context_length=128000,
            capabilities=["chat", "completion"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["gpu"],
        ),
        "command-r-plus": ModelSpec(
            id="command-r-plus",
            name="Command R+",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.TEXT,
            provider=ModelProvider.COHERE,
            parameters=None,
            context_length=128000,
            capabilities=["chat", "completion", "retrieval"],
            quantization_support=["fp16"],
            hardware_accel=["gpu"],
        ),
        "clip": ModelSpec(
            id="clip",
            name="CLIP",
            architecture=ModelArchitecture.TRANSFORMER,
            modality=ModelModality.MULTIMODAL,
            provider=ModelProvider.HUGGINGFACE,
            parameters=428000000,
            context_length=77,
            capabilities=["image_text_matching", "zero_shot_classification"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["gpu", "cpu"],
        ),
        "whisper": ModelSpec(
            id="whisper",
            name="Whisper",
            architecture=ModelArchitecture.ENCODER_DECODER,
            modality=ModelModality.AUDIO,
            provider=ModelProvider.HUGGINGFACE,
            parameters=739000000,
            context_length=4480,
            capabilities=["speech_recognition", "translation"],
            quantization_support=["fp16", "int8", "int4"],
            hardware_accel=["gpu", "cpu"],
        ),
        "stable-diffusion-xl": ModelSpec(
            id="stable-diffusion-xl",
            name="Stable Diffusion XL",
            architecture=ModelArchitecture.DIFFUSION,
            modality=ModelModality.IMAGE,
            provider=ModelProvider.LOCAL,
            parameters=6600000000,
            context_length=77,
            capabilities=["text_to_image", "image_to_image"],
            quantization_support=["fp16", "int8"],
            hardware_accel=["gpu"],
        ),
        "dalle-3": ModelSpec(
            id="dalle-3",
            name="DALL-E 3",
            architecture=ModelArchitecture.DIFFUSION,
            modality=ModelModality.IMAGE,
            provider=ModelProvider.OPENAI,
            parameters=None,
            context_length=4000,
            capabilities=["text_to_image", "image_variation"],
            quantization_support=[],
            hardware_accel=["gpu"],
        ),
    }

    def __init__(self) -> None:
        self._models: dict[str, ModelSpec] = {}
        self._load_defaults()
        logger.info("[ModelRegistry] Initialized with %d models", len(self._models))

    def _load_defaults(self) -> None:
        for model_id, spec in self.KNOWN_MODELS.items():
            self._models[model_id] = spec

    def register_model(self, spec: ModelSpec) -> None:
        self._models[spec.id] = spec

    def get_model(self, model_id: str) -> Optional[ModelSpec]:
        return self._models.get(model_id)

    def list_models(
        self,
        modality: Optional[ModelModality] = None,
        provider: Optional[ModelProvider] = None,
    ) -> list[ModelSpec]:
        models = list(self._models.values())
        if modality:
            models = [m for m in models if m.modality == modality]
        if provider:
            models = [m for m in models if m.provider == provider]
        return models

    def search_models(self, capability: str) -> list[ModelSpec]:
        return [
            m for m in self._models.values()
            if capability.lower() in [c.lower() for c in m.capabilities]
        ]


class InferenceEngine:
    """Unified inference engine for all model types."""

    def __init__(self) -> None:
        self.registry = ModelRegistry()
        self._active_models: dict[str, Any] = {}
        self._inference_history: deque = deque(maxlen=1000)
        logger.info("[InferenceEngine] Initialized")

    def load_model(self, model_id: str) -> bool:
        spec = self.registry.get_model(model_id)
        if not spec:
            logger.error(f"Model not found: {model_id}")
            return False
        
        self._active_models[model_id] = {
            "spec": spec,
            "loaded": True,
            "load_time": 0.0,
        }
        
        logger.info(f"[InferenceEngine] Loaded model: {model_id}")
        return True

    def unload_model(self, model_id: str) -> bool:
        if model_id in self._active_models:
            del self._active_models[model_id]
            return True
        return False

    def infer(self, request: InferenceRequest) -> InferenceResult:
        import time
        start_time = time.time()
        
        if request.model_id not in self._active_models:
            if not self.load_model(request.model_id):
                return InferenceResult(
                    success=False,
                    output=None,
                    model_id=request.model_id,
                    inference_time=time.time() - start_time,
                    error=f"Model not loaded: {request.model_id}",
                )
        
        model = self._active_models[request.model_id]
        spec = model["spec"]
        
        output = self._simulate_inference(request, spec)
        
        result = InferenceResult(
            success=True,
            output=output,
            model_id=request.model_id,
            inference_time=time.time() - start_time,
            tokens_used=len(str(output).split()) if request.modality == ModelModality.TEXT else None,
        )
        
        self._inference_history.append(result)
        
        return result

    def _simulate_inference(self, request: InferenceRequest, spec: ModelSpec) -> Any:
        if request.modality == ModelModality.TEXT:
            return self._generate_text_response(request, spec)
        elif request.modality == ModelModality.IMAGE:
            return {"image_url": "generated_image.png", "model": spec.name}
        elif request.modality == ModelModality.AUDIO:
            return {"audio_url": "generated_audio.wav", "transcript": "Transcribed text"}
        elif request.modality == ModelModality.MULTIMODAL:
            return {"response": "Multi-modal response", "modalities": ["text", "image"]}
        return {"status": "completed"}

    def _generate_text_response(self, request: InferenceRequest, spec: ModelSpec) -> str:
        prompt = str(request.input_data)[:100]
        return f"[{spec.name}] Response to: {prompt}... (temp={request.temperature}, max={request.max_tokens})"

    def get_active_models(self) -> list[str]:
        return list(self._active_models.keys())

    def get_inference_stats(self) -> dict[str, Any]:
        total = len(self._inference_history)
        if total == 0:
            return {"total_inferences": 0, "avg_time": 0.0}
        
        avg_time = sum(r.inference_time for r in self._inference_history) / total
        return {
            "total_inferences": total,
            "avg_inference_time": avg_time,
            "active_models": len(self._active_models),
        }


class ModelOrchestrator:
    """Orchestrates multiple models for complex tasks."""

    def __init__(self) -> None:
        self.engine = InferenceEngine()
        self._workflows: dict[str, dict] = {}
        logger.info("[ModelOrchestrator] Initialized")

    def create_workflow(self, workflow_id: str, steps: list[dict]) -> None:
        self._workflows[workflow_id] = {
            "steps": steps,
            "status": "created",
        }
        logger.info(f"[ModelOrchestrator] Workflow created: {workflow_id}")

    def execute_workflow(self, workflow_id: str, input_data: Any) -> list[InferenceResult]:
        if workflow_id not in self._workflows:
            return []
        
        workflow = self._workflows[workflow_id]
        results = []
        
        for step in workflow["steps"]:
            request = InferenceRequest(
                model_id=step["model"],
                input_data=input_data if step.get("first_step") else results[-1].output if results else input_data,
                modality=ModelModality[step.get("modality", "TEXT")],
                parameters=step.get("parameters", {}),
            )
            result = self.engine.infer(request)
            results.append(result)
        
        return results

    def select_model_for_task(self, task: str, modality: ModelModality) -> Optional[str]:
        if modality == ModelModality.TEXT:
            if "code" in task.lower():
                return "gpt-4"
            elif "reasoning" in task.lower() or "analysis" in task.lower():
                return "claude-3-opus"
            elif "fast" in task.lower() or "simple" in task.lower():
                return "gpt-3.5-turbo"
            elif "large_context" in task.lower():
                return "gemini-1.5-pro"
            return "llama-3-70b"
        
        elif modality == ModelModality.IMAGE:
            return "stable-diffusion-xl"
        
        elif modality == ModelModality.AUDIO:
            return "whisper"
        
        elif modality == ModelModality.MULTIMODAL:
            return "gemini-1.5-pro"
        
        return None


class SuperIntelligence:
    """
    Unified AI integration hub - Super Intelligence Core.
    Combines all AI capabilities into a cohesive system.
    """

    def __init__(self) -> None:
        self.registry = ModelRegistry()
        self.engine = InferenceEngine()
        self.orchestrator = ModelOrchestrator()
        
        self._preferences: dict[str, Any] = {
            "default_text_model": "gpt-4",
            "default_image_model": "stable-diffusion-xl",
            "default_audio_model": "whisper",
            "default_multimodal": "gemini-1.5-pro",
        }
        
        logger.info("[SuperIntelligence] Initialized - All AI models integrated")

    def process(
        self,
        input_data: Any,
        modality: ModelModality,
        model_preference: Optional[str] = None,
        **kwargs,
    ) -> InferenceResult:
        model_id = model_preference or self._preferences.get(
            f"default_{modality.name.lower()}_model"
        )
        
        if not model_id:
            model_id = self.orchestrator.select_model_for_task("", modality)
        
        request = InferenceRequest(
            model_id=model_id,
            input_data=input_data,
            modality=modality,
            parameters=kwargs,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
        )
        
        return self.engine.infer(request)

    def chat(self, message: str, model: Optional[str] = None, **kwargs) -> str:
        result = self.process(
            input_data=message,
            modality=ModelModality.TEXT,
            model_preference=model,
            **kwargs,
        )
        return result.output if result.success else result.error

    def generate_image(self, prompt: str, model: Optional[str] = None) -> dict:
        result = self.process(
            input_data=prompt,
            modality=ModelModality.IMAGE,
            model_preference=model or "stable-diffusion-xl",
        )
        return result.output if result.success else {"error": result.error}

    def transcribe_audio(self, audio_data: Any, model: Optional[str] = None) -> dict:
        result = self.process(
            input_data=audio_data,
            modality=ModelModality.AUDIO,
            model_preference=model or "whisper",
        )
        return result.output if result.success else {"error": result.error}

    def process_multimodal(self, data: dict, model: Optional[str] = None) -> dict:
        result = self.process(
            input_data=data,
            modality=ModelModality.MULTIMODAL,
            model_preference=model or "gemini-1.5-pro",
        )
        return result.output if result.success else {"error": result.error}

    def get_available_models(self, modality: Optional[ModelModality] = None) -> list[dict]:
        models = self.registry.list_models(modality=modality)
        return [
            {
                "id": m.id,
                "name": m.name,
                "modality": m.modality.name,
                "provider": m.provider.value,
                "parameters": m.parameters,
                "context_length": m.context_length,
                "capabilities": m.capabilities,
            }
            for m in models
        ]

    def set_preference(self, key: str, value: str) -> None:
        self._preferences[key] = value

    def get_status(self) -> dict[str, Any]:
        return {
            "preferences": self._preferences,
            "available_models": len(self.registry._models),
            "active_models": len(self.engine._active_models),
            "inference_stats": self.engine.get_inference_stats(),
        }


_super_intelligence: Optional[SuperIntelligence] = None


def get_super_intelligence() -> SuperIntelligence:
    global _super_intelligence
    if _super_intelligence is None:
        _super_intelligence = SuperIntelligence()
    return _super_intelligence


__all__ = [
    "ModelArchitecture",
    "ModelModality",
    "ModelProvider",
    "ModelSpec",
    "InferenceRequest",
    "InferenceResult",
    "ModelRegistry",
    "InferenceEngine",
    "ModelOrchestrator",
    "SuperIntelligence",
    "get_super_intelligence",
]
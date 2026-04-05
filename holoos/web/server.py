from flask import Flask, jsonify, request
from holoos import (
    get_coordinator,
    QuantizationFormat,
    Language,
    QuantizationConfig,
    TranspilerConfig,
    AgentConfig,
    ModelMetadata,
    HoloLayer,
    TensorSpec,
)

app = Flask(__name__)


@app.route("/api/status")
def status():
    return jsonify({"status": "online", "version": "0.1.0"})


@app.route("/api/quantize", methods=["POST"])
def quantize():
    data = request.json
    coord = get_coordinator()
    
    model = ModelMetadata(
        name=data.get("model_name", "test-model"),
        architecture=data.get("architecture", "llama"),
        parameters=data.get("parameters", 7000000000),
    )
    model.layers.append(HoloLayer(
        name="layer_0",
        layer_type="attention",
        tensors={"weight": TensorSpec("weight", "float32", (1024, 1024))}
    ))
    
    config = QuantizationConfig(
        format=QuantizationFormat[data.get("format", "GGUF_Q4_K_M")],
        group_size=data.get("group_size", 128),
    )
    
    result = coord.quantize_model(model, config)
    return jsonify({"status": "success", "format": result.quantization_format.value})


@app.route("/api/transpile", methods=["POST"])
def transpile():
    data = request.json
    coord = get_coordinator()
    
    config = TranspilerConfig(
        source_lang=Language[data.get("source_lang", "PYTHON")],
        target_lang=Language[data.get("target_lang", "RUST")],
    )
    
    result = coord.transpile_code(data.get("code", ""), config)
    return jsonify({"status": "success", "result": result})


@app.route("/api/agent/execute", methods=["POST"])
def agent_execute():
    data = request.json
    coord = get_coordinator()
    
    config = AgentConfig(
        name=data.get("agent_name", "holo-agent"),
        model=data.get("model", "gpt-4"),
        temperature=data.get("temperature", 0.7),
    )
    
    result = coord.execute_agent(data.get("prompt", ""), config)
    return jsonify(result)


@app.route("/api/languages")
def languages():
    return jsonify({"languages": [lang.value for lang in Language]})


@app.route("/api/formats")
def formats():
    return jsonify({"formats": [fmt.name for fmt in QuantizationFormat]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
"""
HoloOS Streaming Responses
==========================
Server-Sent Events for real-time streaming.
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import asyncio
import json
import time


app = FastAPI()


async def stream_chat_response(message: str) -> AsyncGenerator[str, None]:
    """Stream chat response token by token"""
    words = message.split()
    
    for i, word in enumerate(words):
        chunk = {
            "type": "chunk",
            "content": word + " ",
            "index": i,
            "done": False
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.05)
    
    final_chunk = {
        "type": "done",
        "content": "",
        "index": len(words),
        "done": True
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"


async def stream_memory_events() -> AsyncGenerator[str, None]:
    """Stream memory updates in real-time"""
    events = [
        {"type": "memory_load", "level": "semantic", "items": 100},
        {"type": "memory_load", "level": "episodic", "items": 50},
        {"type": "memory_load", "level": "working", "items": 7},
        {"type": "memory_load", "level": "procedural", "items": 25},
        {"type": "memory_ready", "total": 182},
    ]
    
    for event in events:
        yield f"data: {json.dumps(event)}\n\n"
        await asyncio.sleep(0.3)


async def stream_metrics() -> AsyncGenerator[str, None]:
    """Stream system metrics"""
    while True:
        metrics = {
            "type": "metrics",
            "cpu": 40 + (time.time() % 20),
            "memory": 50 + (time.time() % 15),
            "disk": 35,
            "requests": int(time.time() % 1000),
            "timestamp": time.time()
        }
        yield f"data: {json.dumps(metrics)}\n\n"
        await asyncio.sleep(2)


async def stream_logs() -> AsyncGenerator[str, None]:
    """Stream system logs"""
    log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
    messages = [
        "System initialized",
        "Loading modules",
        "Kernel ready",
        "AI Hub connected",
        "Memory system ready",
        "All systems online"
    ]
    
    for i, msg in enumerate(messages):
        log = {
            "type": "log",
            "level": log_levels[i % len(log_levels)],
            "message": msg,
            "timestamp": time.time()
        }
        yield f"data: {json.dumps(log)}\n\n"
        await asyncio.sleep(0.5)


@app.get("/api/stream/chat")
async def stream_chat():
    async def generate():
        async for chunk in stream_chat_response("HoloOS está processando sua solicitação com streaming de resposta em tempo real."):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/stream/memory")
async def stream_memory():
    async def generate():
        async for event in stream_memory_events():
            yield event
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/stream/metrics")
async def stream_metrics_endpoint():
    async def generate():
        async for event in stream_metrics():
            yield event
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/stream/logs")
async def stream_logs_endpoint():
    async def generate():
        async for log in stream_logs():
            yield log
    
    return StreamingResponse(generate(), media_type="text/event-stream")


__all__ = ["stream_chat_response", "stream_memory_events", "stream_metrics", "stream_logs"]
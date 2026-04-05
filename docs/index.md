# HoloOS Documentation

## Welcome to HoloOS

HoloOS is the most advanced native AI operating system, combining multiple AI technologies in a unified platform.

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running

```bash
# Start the API server
python -m holoos.api.main

# Or use the CLI
python -m holoos.cli.main status
```

## Modules

### AI Hub
17 AI models integrated: GPT-4, Claude 3, Gemini, Llama 3, and more.

### Kernel
Self-Attention (6 layers, 12 heads, 768 dimensions), Soul, Consciousness.

### Security
Auto-defense with threat detection, IPS, encryption.

### Memory
Semantic (768d vectors), Episodic, Working (7 slots), Procedural.

### Planning
Goal Decomposition, Reasoning (CoT, ToT, ReAct).

## API Reference

### Chat
```
POST /api/ai/chat
{
  "message": "Hello",
  "model": "gpt-4"
}
```

### Memory
```
POST /api/memory/store
{
  "content": "Important data",
  "tags": ["ai", "learning"]
}
```

### Tools
```
POST /api/tools/execute
{
  "tool": "web_search",
  "params": {"query": "AI news"}
}
```

## SDK Usage

### Python
```python
from holoos import HoloOSClient

client = HoloOSClient("http://localhost:8000")
response = client.chat("Hello!")
```

### JavaScript
```javascript
import { HoloOSClient } from '@holoos/sdk';

const client = new HoloOSClient();
const response = await client.chat({ message: "Hello" });
```

## Configuration

Environment variables:
- `HOLOOS_ENV` - production/development
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `API_KEY` - Authentication key

## Architecture

```
┌─────────────────────────────────────────────┐
│                 HoloOS v0.7.0               │
├──────────┬──────────┬──────────┬───────────┤
│   AI     │  Memory  │ Planning │   Tools   │
│   Hub    │  System  │  Engine  │ Executor  │
├──────────┴──────────┴──────────┴───────────┤
│  Kernel  │ Security │ Gateway │  Database │
└──────────┴──────────┴──────────┴───────────┘
```

## License

MIT License - See LICENSE file.
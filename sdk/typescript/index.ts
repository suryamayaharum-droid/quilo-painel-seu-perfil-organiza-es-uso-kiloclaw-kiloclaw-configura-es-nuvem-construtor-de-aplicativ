/**
 * HoloOS TypeScript SDK
 * =====================
 * Full type-safe SDK for JavaScript/TypeScript
 */

export type ModelId = 
  | "gpt-4" 
  | "gpt-3.5" 
  | "claude-3" 
  | "claude-sonnet" 
  | "gemini-pro" 
  | "gemini-flash" 
  | "llama-3" 
  | "mistral" 
  | "command-r";

export interface ChatRequest {
  message: string;
  model?: ModelId;
  temperature?: number;
  maxTokens?: number;
}

export interface ChatResponse {
  response: string;
  model: string;
  usage?: {
    prompt: number;
    completion: number;
    total: number;
  };
}

export interface MemoryItem {
  id: string;
  content: string;
  tags: string[];
  timestamp: string;
}

export interface MemoryStoreRequest {
  content: string;
  tags?: string[];
}

export interface MemoryQueryRequest {
  query: string;
  limit?: number;
}

export interface ToolRequest {
  tool: string;
  params: Record<string, unknown>;
}

export interface ToolResponse {
  status: string;
  result: unknown;
  tool: string;
}

export interface GoalRequest {
  description: string;
  strategy?: "chain_of_thought" | "tree_of_thought" | "react";
}

export interface GoalResponse {
  goal: string;
  plan: string[];
  status: string;
}

export interface Metrics {
  cpu: number;
  memory: number;
  disk: number;
  requests: number;
  errors: number;
  uptime: string;
}

export interface SecurityStatus {
  level: "low" | "medium" | "high" | "critical";
  threats_detected: number;
  policies: string[];
  active: boolean;
}

export interface Module {
  name: string;
  status: "online" | "offline" | "error";
  info?: string;
}

export interface Model {
  id: string;
  name: string;
  provider: string;
}

export interface Tool {
  name: string;
  description: string;
}

export interface LogEntry {
  level: "debug" | "info" | "warning" | "error";
  message: string;
  timestamp: string;
}

export interface Config {
  key: string;
  value: unknown;
}

export interface Plugin {
  name: string;
  version: string;
  enabled: boolean;
}

export type EventType = 
  | "chat.message" 
  | "memory.stored" 
  | "goal.created" 
  | "tool.executed" 
  | "security.alert";

export interface WebhookEvent {
  type: EventType;
  payload: Record<string, unknown>;
  timestamp: string;
}

export interface FunctionDefinition {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
}

export interface FunctionCallRequest {
  function: string;
  arguments: Record<string, unknown>;
}

export interface FunctionCallResponse {
  id: string;
  function: string;
  status: "pending" | "running" | "success" | "error";
  result?: unknown;
  error?: string;
}

export class HoloOSClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(baseUrl: string = "http://localhost:8000", apiKey?: string) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (this.apiKey) {
      headers["Authorization"] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // AI Methods
  async chat(request: ChatRequest): Promise<ChatResponse> {
    return this.request<ChatResponse>("/api/ai/chat", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async complete(prompt: string, model?: ModelId): Promise<{ completion: string }> {
    return this.request<{ completion: string }>("/api/ai/complete", {
      method: "POST",
      body: JSON.stringify({ message: prompt, model }),
    });
  }

  async listModels(): Promise<{ models: Model[] }> {
    return this.request<{ models: Model[] }>("/api/ai/models");
  }

  // Memory Methods
  async storeMemory(request: MemoryStoreRequest): Promise<{ status: string }> {
    return this.request<{ status: string }>("/api/memory/store", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async retrieveMemory(request: MemoryQueryRequest): Promise<{ results: MemoryItem[] }> {
    const params = new URLSearchParams({
      query: request.query,
      limit: String(request.limit || 5),
    });
    return this.request<{ results: MemoryItem[] }>(`/api/memory/retrieve?${params}`);
  }

  async getMemoryStats(): Promise<{
    semantic: { items: number; dimensions: number };
    episodic: { items: number };
    working: { items: number; capacity: number };
    procedural: { skills: number };
  }> {
    return this.request("/api/memory/stats");
  }

  // Tools Methods
  async executeTool(request: ToolRequest): Promise<ToolResponse> {
    return this.request<ToolResponse>("/api/tools/execute", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async listTools(): Promise<{ tools: Tool[] }> {
    return this.request<{ tools: Tool[] }>("/api/tools");
  }

  // Planning Methods
  async createGoal(request: GoalRequest): Promise<GoalResponse> {
    return this.request<GoalResponse>("/api/planning/goal", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async listGoals(): Promise<{ goals: unknown[] }> {
    return this.request<{ goals: unknown[] }>("/api/planning/goals");
  }

  // Security Methods
  async getSecurityStatus(): Promise<SecurityStatus> {
    return this.request<SecurityStatus>("/api/security/status");
  }

  async listThreats(): Promise<{ threats: unknown[] }> {
    return this.request<{ threats: unknown[] }>("/api/security/threats");
  }

  // Monitoring Methods
  async getMetrics(): Promise<Metrics> {
    return this.request<Metrics>("/api/monitoring/metrics");
  }

  async getLogs(level?: string, limit?: number): Promise<{ logs: LogEntry[] }> {
    const params = new URLSearchParams();
    if (level) params.set("level", level);
    if (limit) params.set("limit", String(limit));
    return this.request<{ logs: LogEntry[] }>(`/api/monitoring/logs?${params}`);
  }

  // Config Methods
  async setConfig(key: string, value: unknown): Promise<{ status: string }> {
    return this.request<{ status: string }>("/api/config", {
      method: "POST",
      body: JSON.stringify({ key, value }),
    });
  }

  async getConfig(key: string): Promise<Config> {
    return this.request<Config>(`/api/config?key=${key}`);
  }

  // Module Methods
  async listModules(): Promise<{ modules: Module[] }> {
    return this.request<{ modules: Module[] }>("/api/modules");
  }

  // Plugin Methods
  async installPlugin(name: string): Promise<{ status: string }> {
    return this.request<{ status: string }>("/api/plugins/install", {
      method: "POST",
      body: JSON.stringify({ name }),
    });
  }

  async listPlugins(): Promise<{ plugins: Plugin[] }> {
    return this.request<{ plugins: Plugin[] }>("/api/plugins");
  }

  // WebSocket Methods
  connectWebSocket(callback: (data: unknown) => void): WebSocket {
    const ws = new WebSocket(`${this.baseUrl.replace("http", "ws")}/ws`);
    ws.onmessage = (event) => {
      callback(JSON.parse(event.data));
    };
    return ws;
  }

  // Streaming Methods
  async *streamChat(message: string): AsyncGenerator<string> {
    const response = await fetch(`${this.baseUrl}/api/stream/chat`);
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) return;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");
      
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = JSON.parse(line.slice(6));
          yield data.content;
          if (data.done) return;
        }
      }
    }
  }

  // Function Calling
  async callFunction(request: FunctionCallRequest): Promise<FunctionCallResponse> {
    return this.request<FunctionCallResponse>("/api/functions/execute", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async listFunctions(): Promise<{ functions: FunctionDefinition[] }> {
    return this.request<{ functions: FunctionDefinition[] }>("/api/functions");
  }

  // Health Check
  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>("/health");
  }
}

// Export singleton factory
export function createClient(baseUrl?: string, apiKey?: string): HoloOSClient {
  return new HoloOSClient(baseUrl, apiKey);
}

export default HoloOSClient;
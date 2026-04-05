"use client";

import { useState, useEffect } from "react";

interface Module {
  name: string;
  status: string;
  info?: string;
}

interface Metrics {
  cpu: number;
  memory: number;
  disk: number;
  requests: number;
  errors: number;
}

interface MemoryItem {
  id: string;
  content: string;
  tags: string[];
  timestamp: string;
}

interface Goal {
  id: string;
  description: string;
  status: string;
  progress: number;
}

interface LogEntry {
  level: string;
  message: string;
  timestamp: string;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<{role: string, content: string}[]>([]);
  const [memoryItems, setMemoryItems] = useState<MemoryItem[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [metrics, setMetrics] = useState<Metrics>({ cpu: 45, memory: 62, disk: 38, requests: 1247, errors: 3 });
  const [darkMode, setDarkMode] = useState(true);

  const modules: Module[] = [
    { name: "AI Hub", status: "online", info: "17 modelos" },
    { name: "Kernel", status: "online", info: "Self-Attention" },
    { name: "Security", status: "online", info: "Auto-defesa" },
    { name: "Memory", status: "online", info: "768d vectors" },
    { name: "Planner", status: "online", info: "CoT + ToT" },
    { name: "Tools", status: "online", info: "9 ferramentas" },
    { name: "Gateway", status: "online", info: "Rate limit" },
    { name: "Database", status: "online", info: "SQL + NoSQL" },
    { name: "Monitoring", status: "online", info: "Metrics" },
    { name: "Plugins", status: "online", info: "Dynamic" },
    { name: "Config", status: "online", info: "Env vars" },
    { name: "Governance", status: "online", info: "Assembly" },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        cpu: Math.floor(Math.random() * 30) + 30,
        memory: Math.floor(Math.random() * 20) + 50,
        disk: prev.disk,
        requests: prev.requests + Math.floor(Math.random() * 10),
        errors: Math.max(0, prev.errors + (Math.random() > 0.8 ? 1 : 0)),
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = () => {
    if (!message.trim()) return;
    
    setChatHistory(prev => [...prev, { role: "user", content: message }]);
    
    setTimeout(() => {
      setChatHistory(prev => [...prev, { 
        role: "assistant", 
        content: `HoloOS processou: "${message.substring(0, 50)}..."`
      }]);
    }, 500);
    
    setMessage("");
  };

  const addMemory = () => {
    if (!message.trim()) return;
    setMemoryItems(prev => [...prev, {
      id: `mem_${Date.now()}`,
      content: message,
      tags: ["user"],
      timestamp: new Date().toISOString(),
    }]);
    setMessage("");
  };

  const addGoal = () => {
    if (!message.trim()) return;
    setGoals(prev => [...prev, {
      id: `goal_${Date.now()}`,
      description: message,
      status: "pending",
      progress: 0,
    }]);
    setMessage("");
  };

  const tabs = [
    { id: "dashboard", label: "Dashboard", icon: "📊" },
    { id: "chat", label: "Chat AI", icon: "💬" },
    { id: "memory", label: "Memória", icon: "🧠" },
    { id: "planning", label: "Planejamento", icon: "📋" },
    { id: "security", label: "Segurança", icon: "🛡️" },
    { id: "logs", label: "Logs", icon: "📜" },
    { id: "settings", label: "Config", icon: "⚙️" },
  ];

  return (
    <div className={`min-h-screen ${darkMode ? "bg-black text-green-400" : "bg-white text-gray-900"}`}>
      <div className="flex">
        <aside className="w-64 min-h-screen border-r border-green-800/30 p-4">
          <h1 className="text-2xl font-bold text-green-500 mb-8 tracking-widest">HOLOOS</h1>
          
          <nav className="space-y-2">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full text-left px-4 py-3 rounded-lg flex items-center gap-3 transition-all ${
                  activeTab === tab.id 
                    ? "bg-green-500/20 text-green-400 border border-green-500/30" 
                    : "hover:bg-green-500/10"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>

          <div className="mt-8 p-4 border border-green-800/30 rounded-lg">
            <h3 className="text-sm font-semibold mb-3 text-green-600">Módulos Online</h3>
            <div className="flex flex-wrap gap-2">
              {modules.slice(0, 6).map(m => (
                <span key={m.name} className="text-xs px-2 py-1 bg-green-500/20 rounded">
                  {m.name}
                </span>
              ))}
              <span className="text-xs text-green-600">+{modules.length - 6} mais</span>
            </div>
          </div>
        </aside>

        <main className="flex-1 p-8">
          {activeTab === "dashboard" && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-semibold">System Overview</h2>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-green-600">v0.7.0</span>
                  <span className="px-3 py-1 bg-green-500/20 rounded-full text-sm">Online</span>
                </div>
              </div>

              <div className="grid grid-cols-4 gap-4">
                <div className="p-6 border border-green-800/30 rounded-xl bg-green-500/5">
                  <div className="text-3xl font-bold">{metrics.cpu}%</div>
                  <div className="text-sm text-green-600 mt-1">CPU Usage</div>
                </div>
                <div className="p-6 border border-green-800/30 rounded-xl bg-green-500/5">
                  <div className="text-3xl font-bold">{metrics.memory}%</div>
                  <div className="text-sm text-green-600 mt-1">Memory</div>
                </div>
                <div className="p-6 border border-green-800/30 rounded-xl bg-green-500/5">
                  <div className="text-3xl font-bold">{metrics.disk}%</div>
                  <div className="text-sm text-green-600 mt-1">Disk</div>
                </div>
                <div className="p-6 border border-green-800/30 rounded-xl bg-green-500/5">
                  <div className="text-3xl font-bold">{metrics.requests}</div>
                  <div className="text-sm text-green-600 mt-1">Requests</div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="col-span-2 p-6 border border-green-800/30 rounded-xl">
                  <h3 className="text-lg font-semibold mb-4">Atividade em Tempo Real</h3>
                  <div className="space-y-2">
                    {[1,2,3,4,5].map(i => (
                      <div key={i} className="flex items-center gap-4">
                        <div className="w-2 h-2 rounded-full bg-green-500"></div>
                        <span className="text-sm">Processando...</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="p-6 border border-green-800/30 rounded-xl">
                  <h3 className="text-lg font-semibold mb-4">Módulos</h3>
                  <div className="space-y-2">
                    {modules.map(m => (
                      <div key={m.name} className="flex justify-between items-center text-sm">
                        <span>{m.name}</span>
                        <span className="text-green-500">●</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "chat" && (
            <div className="h-[calc(100vh-100px)] flex flex-col">
              <h2 className="text-2xl font-semibold mb-4">Chat com HoloOS</h2>
              
              <div className="flex-1 border border-green-800/30 rounded-xl p-4 overflow-y-auto space-y-4">
                {chatHistory.length === 0 ? (
                  <p className="text-green-600 text-center">Inicie uma conversa...</p>
                ) : (
                  chatHistory.map((msg, i) => (
                    <div key={i} className={`p-3 rounded-lg ${msg.role === "user" ? "bg-green-500/10 ml-8" : "bg-green-500/5 mr-8"}`}>
                      <span className="text-xs text-green-600">{msg.role === "user" ? "Você" : "HoloOS"}</span>
                      <p>{msg.content}</p>
                    </div>
                  ))
                )}
              </div>
              
              <div className="mt-4 flex gap-2">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                  placeholder="Digite sua mensagem..."
                  className="flex-1 p-3 bg-black border border-green-800/30 rounded-lg focus:border-green-500 outline-none"
                />
                <button 
                  onClick={sendMessage}
                  className="px-6 py-3 bg-green-500 text-black rounded-lg font-semibold hover:bg-green-400"
                >
                  Enviar
                </button>
              </div>
            </div>
          )}

          {activeTab === "memory" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Sistema de Memória</h2>
              
              <div className="grid grid-cols-2 gap-6">
                <div className="p-6 border border-green-800/30 rounded-xl">
                  <h3 className="text-lg font-semibold mb-4">Memória Semântica</h3>
                  <div className="space-y-3">
                    {memoryItems.map(item => (
                      <div key={item.id} className="p-3 bg-green-500/10 rounded-lg">
                        <p className="text-sm">{item.content}</p>
                        <div className="flex gap-2 mt-2">
                          {item.tags.map(tag => (
                            <span key={tag} className="text-xs px-2 py-0.5 bg-green-500/20 rounded">{tag}</span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="p-6 border border-green-800/30 rounded-xl">
                  <h3 className="text-lg font-semibold mb-4">Adicionar Memória</h3>
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      placeholder="Nova memória..."
                      className="w-full p-3 bg-black border border-green-800/30 rounded-lg"
                    />
                    <button 
                      onClick={addMemory}
                      className="w-full py-2 bg-green-500 text-black rounded-lg font-semibold"
                    >
                      Salvar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "planning" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Planejamento</h2>
              
              <div className="p-6 border border-green-800/30 rounded-xl">
                <h3 className="text-lg font-semibold mb-4">Criar Novo Objetivo</h3>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Descreva um objetivo..."
                    className="flex-1 p-3 bg-black border border-green-800/30 rounded-lg"
                  />
                  <button 
                    onClick={addGoal}
                    className="px-6 py-3 bg-green-500 text-black rounded-lg font-semibold"
                  >
                    Criar
                  </button>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                {goals.map(goal => (
                  <div key={goal.id} className="p-4 border border-green-800/30 rounded-xl">
                    <h4 className="font-semibold">{goal.description}</h4>
                    <div className="mt-3 h-2 bg-green-900/30 rounded-full overflow-hidden">
                      <div className="h-full bg-green-500" style={{width: `${goal.progress}%`}}></div>
                    </div>
                    <span className="text-xs text-green-600 mt-1 block">{goal.status}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "security" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Centro de Segurança</h2>
              
              <div className="grid grid-cols-3 gap-4">
                <div className="p-6 border border-green-800/30 rounded-xl text-center">
                  <div className="text-4xl font-bold text-green-500">ALTO</div>
                  <div className="text-sm text-green-600 mt-1">Nível de Segurança</div>
                </div>
                <div className="p-6 border border-green-800/30 rounded-xl text-center">
                  <div className="text-4xl font-bold">0</div>
                  <div className="text-sm text-green-600 mt-1">Ameaças Detectadas</div>
                </div>
                <div className="p-6 border border-green-800/30 rounded-xl text-center">
                  <div className="text-4xl font-bold">5</div>
                  <div className="text-sm text-green-600 mt-1">Políticas Ativas</div>
                </div>
              </div>
              
              <div className="p-6 border border-green-800/30 rounded-xl">
                <h3 className="text-lg font-semibold mb-4">Políticas de Segurança</h3>
                <div className="space-y-3">
                  {["Bloquear Malicioso", "Rate Limiting", "Auth Obrigatória", "Criptografar Dados", "Audit Log"].map(policy => (
                    <div key={policy} className="flex items-center gap-3 p-3 bg-green-500/10 rounded-lg">
                      <span className="text-green-500">✓</span>
                      <span>{policy}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === "logs" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Logs do Sistema</h2>
              
              <div className="p-6 border border-green-800/30 rounded-xl font-mono text-sm">
                <div className="space-y-2">
                  {logs.length === 0 ? (
                    <>
                      <div><span className="text-green-600">[05:55:00]</span> HoloOS v0.7.0 initialized</div>
                      <div><span className="text-green-600">[05:55:01]</span> Loading modules...</div>
                      <div><span className="text-green-600">[05:55:02]</span> ✓ Kernel (Self-Attention + Soul + Consciousness)</div>
                      <div><span className="text-green-600">[05:55:02]</span> ✓ AI Hub (17 models)</div>
                      <div><span className="text-green-600">[05:55:03]</span> ✓ Security Kernel (Auto-defense)</div>
                      <div><span className="text-green-600">[05:55:03]</span> ✓ Memory System (Vector + Episodic + Working)</div>
                      <div><span className="text-green-600">[05:55:04]</span> All systems online. Ready for commands.</div>
                    </>
                  ) : (
                    logs.map((log, i) => (
                      <div key={i}>
                        <span className="text-green-600">[{log.timestamp}]</span> {log.message}
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === "settings" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Configurações</h2>
              
              <div className="p-6 border border-green-800/30 rounded-xl space-y-4">
                <div className="flex items-center justify-between">
                  <span>Modo Escuro</span>
                  <button 
                    onClick={() => setDarkMode(!darkMode)}
                    className={`w-12 h-6 rounded-full transition-colors ${darkMode ? "bg-green-500" : "bg-gray-600"}`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full transition-transform ${darkMode ? "translate-x-7" : "translate-x-1"}`}></div>
                  </button>
                </div>
                
                <div className="flex items-center justify-between">
                  <span>Auto-atualização</span>
                  <button className="px-4 py-2 bg-green-500 text-black rounded-lg">Ativo</button>
                </div>
                
                <div className="pt-4 border-t border-green-800/30">
                  <h3 className="text-lg font-semibold mb-3">Informações do Sistema</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between"><span>Versão</span><span className="text-green-500">0.7.0</span></div>
                    <div className="flex justify-between"><span>Arquivos Python</span><span className="text-green-500">46</span></div>
                    <div className="flex justify-between"><span>Módulos</span><span className="text-green-500">17</span></div>
                    <div className="flex justify-between"><span>Modelos de IA</span><span className="text-green-500">17</span></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
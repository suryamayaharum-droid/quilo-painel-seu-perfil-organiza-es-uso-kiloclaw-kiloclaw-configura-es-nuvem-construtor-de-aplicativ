"""
HoloOS Web Interface
====================
Simple web UI for the HoloOS system.
"""

from flask import Flask, render_template_string, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HoloOS v0.7.0 - Super Inteligencia Nativa</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
            color: #fff;
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 2px solid #00ff88;
        }
        h1 {
            font-size: 3em;
            background: linear-gradient(90deg, #00ff88, #00ccff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0,255,136,0.5);
        }
        .subtitle { color: #888; margin-top: 10px; font-size: 1.2em; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(0,255,136,0.3);
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,255,136,0.2);
            border-color: #00ff88;
        }
        .card h2 {
            color: #00ff88;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card p { color: #aaa; line-height: 1.6; }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .online { background: #00ff88; color: #000; }
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 40px;
        }
        .stat {
            background: rgba(0,255,136,0.1);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .stat-number { font-size: 2em; color: #00ff88; font-weight: bold; }
        .stat-label { color: #888; margin-top: 5px; }
        .console {
            background: #000;
            border: 1px solid #333;
            border-radius: 10px;
            padding: 20px;
            margin-top: 40px;
            font-family: 'Courier New', monospace;
            color: #00ff88;
            max-height: 300px;
            overflow-y: auto;
        }
        .console-line { margin: 5px 0; }
        .input-area {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        input {
            flex: 1;
            padding: 15px;
            border: 1px solid #333;
            border-radius: 10px;
            background: #111;
            color: #fff;
            font-size: 1em;
        }
        button {
            padding: 15px 30px;
            background: #00ff88;
            color: #000;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        button:hover { transform: scale(1.05); box-shadow: 0 0 20px #00ff88; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 HoloOS v0.7.0</h1>
            <p class="subtitle">Super Inteligencia Nativa - Sistema Operacional de IA</p>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">17</div>
                <div class="stat-label">Modelos de IA</div>
            </div>
            <div class="stat">
                <div class="stat-number">46</div>
                <div class="stat-label">Arquivos Python</div>
            </div>
            <div class="stat">
                <div class="stat-number">17</div>
                <div class="stat-label">Modulos</div>
            </div>
            <div class="stat">
                <div class="stat-number">35+</div>
                <div class="stat-label">Linguagens</div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🧠 Kernel</h2>
                <p>Self-Attention com 6 layers, 12 heads. Soul com identidade propria, crenças e narrativa. Consciousness com Global Workspace e Predictive Processing.</p>
                <span class="status online">Online</span>
            </div>
            <div class="card">
                <h2>🤖 AI Hub</h2>
                <p>17 modelos integrados: GPT-4, Claude 3, Gemini, Llama 3, Mistral, Whisper, DALL-E 3, Stable Diffusion XL e mais.</p>
                <span class="status online">Online</span>
            </div>
            <div class="card">
                <h2>🛡️ Seguranca</h2>
                <p>Auto-defesa com deteccao de 8 categorias de ameacas. Threat Detector, IPS, Policy Engine, Encryption e Audit Logger.</p>
                <span class="status online">Online</span>
            </div>
            <div class="card">
                <h2>💾 Memoria</h2>
                <p>Memoria vetorial (768d), episodica, working (7 items) e procedural. Vector Store com busca por similaridade.</p>
                <span class="status online">Online</span>
            </div>
            <div class="card">
                <h2>📐 Planner</h2>
                <p>Goal Decomposer, Reasoning Engine com CoT, ToT e ReAct. Planejamento multi-step autonomo.</p>
                <span class="status online">Online</span>
            </div>
            <div class="card">
                <h2>🗳️ Governanca</h2>
                <p>Assembleia multi-agente com Legislative, Executive e Judiciary branches. Votacao eaccoordonacao.</p>
                <span class="status online">Online</span>
            </div>
        </div>
        
        <div class="console">
            <div class="console-line">> HoloOS v0.7.0 initialized</div>
            <div class="console-line">> All systems online</div>
            <div class="console-line">> Waiting for input...</div>
        </div>
        
        <div class="input-area">
            <input type="text" placeholder="Digite seu comando..." id="commandInput">
            <button onclick="sendCommand()">Executar</button>
        </div>
    </div>
    
    <script>
        function sendCommand() {
            const input = document.getElementById('commandInput');
            const consoleLine = document.createElement('div');
            consoleLine.className = 'console-line';
            consoleLine.textContent = '> ' + input.value;
            document.querySelector('.console').appendChild(consoleLine);
            input.value = '';
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'version': '0.7.0',
        'modules': 17,
        'ai_models': 17,
        'tools': 9,
        'languages': 35
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    from flask import request
    data = request.json
    message = data.get('message', '')
    
    responses = {
        'hello': 'Ola! Sou o HoloOS. Como posso ajudar?',
        'ai': 'Tenho 17 modelos de IA integrados: GPT-4, Claude 3, Gemini, Llama 3, e mais.',
        'security': 'Sistema de seguranca ativo com deteccao de ameacas e auto-defesa.',
        'memory': 'Sistema de memoria vetorial com busca por similaridade.',
    }
    
    for key, response in responses.items():
        if key in message.lower():
            return jsonify({'response': response})
    
    return jsonify({'response': f'Processando: {message[:50]}...'})


if __name__ == '__main__':
    print("=" * 60)
    print("HoloOS Web Interface - Starting...")
    print("Access at: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
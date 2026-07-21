import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, Settings, Users, Activity, Plus, Hash, Send, 
  TerminalSquare, CheckCircle2, Clock, 
  ShieldAlert, Beaker, Terminal, Code2, Database, Layout, 
  TestTube2, GitMerge, AlertTriangle, Check, X, Copy, PlayCircle,
  Loader2, Cpu, CheckSquare
} from 'lucide-react';

const SWARM_AGENTS = [
  { id: 'gini', name: 'Gini', role: 'Router Principal', status: 'idle', color: 'text-fuchsia-400', bg: 'bg-fuchsia-500/10', icon: GitMerge },
  { id: 'evo', name: 'Evo', role: 'Arqui. Mutación', status: 'waiting', color: 'text-orange-500', bg: 'bg-orange-500/10', icon: Beaker },
  { id: 'yimi', name: 'Yimi', role: 'Product Owner', status: 'idle', color: 'text-blue-400', bg: 'bg-blue-500/10', icon: Layout },
  { id: 'fani', name: 'Fani', role: 'Frontend Dev', status: 'completed', color: 'text-pink-400', bg: 'bg-pink-500/10', icon: Code2 },
  { id: 'cami', name: 'Cami', role: 'Backend Dev', status: 'processing', color: 'text-emerald-400', bg: 'bg-emerald-500/10', icon: Terminal },
  { id: 'mani', name: 'Mani', role: 'QA Automation', status: 'error', color: 'text-red-400', bg: 'bg-red-500/10', icon: TestTube2 },
  { id: 'romi', name: 'Romi', role: 'DevSecOps', status: 'idle', color: 'text-violet-400', bg: 'bg-violet-500/10', icon: ShieldAlert },
  { id: 'sefi', name: 'Sefi', role: 'Data Engineer', status: 'idle', color: 'text-cyan-400', bg: 'bg-cyan-500/10', icon: Database },
];

const INITIAL_JOURNEY = [
  { 
    id: 1, type: 'user', 
    text: 'Construye el frontend y backend de una calculadora de préstamos.' 
  },
  { 
    id: 2, type: 'gini_routing', 
    text: 'Analizando requerimiento arquitectónico. Dividiendo la tarea en hilos paralelos: Asignando la interfaz React a @Fani y la API de cálculo financiero a @Cami. Iniciando orquestación...' 
  },
  { 
    id: 3, type: 'action_card', agentId: 'fani', status: 'awaiting_approval',
    reflection: 'Auto-Auditoría: Inicialmente utilicé botones de bajo contraste. He modificado la paleta a estándares WCAG AAA para garantizar máxima accesibilidad antes de la entrega.',
    strategy: 'He desarrollado un componente funcional en React utilizando Tailwind CSS para la grilla responsiva de la calculadora. Los estados están listos para conectarse con la API.',
    code: `export default function CalculatorUI() {\n  const [amount, setAmount] = useState(0);\n  return (\n    <div className="p-4 grid grid-cols-4 gap-2">\n      {/* UI Implementation */}\n    </div>\n  );\n}`,
    terminalLogs: []
  },
  { 
    id: 4, type: 'action_card', agentId: 'cami', status: 'processing',
    text: 'Estructurando arquitectura de API...' 
  },
  {
    id: 5, type: 'evo_alert', agentId: 'mani',
    text: 'Fallo cognitivo detectado durante el setup de Cypress. Conocimiento desactualizado en la versión 13.x. Solicitando intervención de EVO para mutación de cerebro XML en caliente.'
  }
];

export default function SwarmOrchestrator() {
  const [inputText, setInputText] = useState('');
  const [activeTab, setActiveTab] = useState('chat');
  const [journey, setJourney] = useState(INITIAL_JOURNEY);

  // Simulación de inyección de código y terminal interactiva
  const handleApprove = (blockId) => {
    setJourney(prev => prev.map(block => {
      if (block.id === blockId) {
        return { ...block, status: 'executing', terminalLogs: ['Iniciando inyección en máquina física...'] };
      }
      return block;
    }));

    // Simular logs llegando asíncronamente
    const logs = [
      '[OK] Validando dependencias de React...',
      '[OK] Escribiendo CalculatorUI.jsx en src/components/',
      '[OK] Actualizando rutas de index.js...',
      '[EXITO] Módulo compilado y desplegado correctamente en localhost:3000.'
    ];

    logs.forEach((log, index) => {
      setTimeout(() => {
        setJourney(prev => prev.map(block => {
          if (block.id === blockId) {
            const currentLogs = block.terminalLogs || [];
            const newStatus = index === logs.length - 1 ? 'deployed' : 'executing';
            return { ...block, status: newStatus, terminalLogs: [...currentLogs, log] };
          }
          return block;
        }));
      }, (index + 1) * 800);
    });
  };

  return (
    <div className="flex h-screen w-full bg-[#0B0F19] text-slate-300 font-sans overflow-hidden">
      
      {/* PANEL IZQUIERDO: Navegación Corporativa */}
      <aside className="w-64 bg-[#111827] border-r border-slate-800/60 flex flex-col z-20 shadow-xl">
        <div className="p-5 border-b border-slate-800/60">
          <div className="flex items-center gap-3 text-white font-bold text-xl tracking-tight">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center border border-indigo-500/30">
              <Activity className="w-5 h-5 text-indigo-400" />
            </div>
            <span>Gini <span className="text-indigo-400 font-light">V8.0</span></span>
          </div>
        </div>
        
        <div className="p-4">
          <button className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white py-2.5 px-4 rounded-md transition-all text-sm font-medium shadow-[0_0_15px_rgba(79,70,229,0.3)] hover:shadow-[0_0_25px_rgba(79,70,229,0.5)]">
            <Plus className="w-4 h-4" />
            Nuevo Hilo Operativo
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3 py-2">
          <div className="text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-3 px-2">
            Sesiones Activas
          </div>
          <div className="space-y-1">
            <button className="w-full flex items-center gap-3 px-3 py-2.5 text-left rounded-md bg-slate-800/50 border border-slate-700/50 text-indigo-300 shadow-inner">
              <Hash className="w-4 h-4 shrink-0" />
              <div className="truncate text-sm font-medium">Calculadora Financiera</div>
            </button>
            <button className="w-full flex items-center gap-3 px-3 py-2.5 text-left rounded-md hover:bg-slate-800/30 text-slate-400 transition-colors">
              <Hash className="w-4 h-4 shrink-0" />
              <div className="truncate text-sm">Refactorización API Auth</div>
            </button>
          </div>
        </div>

        <div className="p-4 border-t border-slate-800/60 bg-[#0B0F19]/50">
          <button className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors text-sm w-full">
            <Settings className="w-4 h-4" />
            Ajustes del Enjambre
          </button>
        </div>
      </aside>

      {/* ÁREA CENTRAL */}
      <main className="flex-1 flex flex-col bg-[#0B0F19] relative">
        
        {/* TABS SUPERIORES */}
        <header className="h-14 border-b border-slate-800/60 flex items-end px-6 bg-[#111827] z-10 gap-6">
          <button 
            onClick={() => setActiveTab('chat')}
            className={`pb-3 px-2 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'chat' ? 'border-indigo-500 text-indigo-400' : 'border-transparent text-slate-400 hover:text-slate-200'}`}
          >
            <TerminalSquare className="w-4 h-4" /> Panel de Orquestación
          </button>
          <button 
            onClick={() => setActiveTab('evo')}
            className={`pb-3 px-2 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'evo' ? 'border-orange-500 text-orange-400' : 'border-transparent text-slate-400 hover:text-orange-300'}`}
          >
            <Beaker className="w-4 h-4" /> Laboratorio Evo
          </button>
          <button 
            onClick={() => setActiveTab('security')}
            className={`pb-3 px-2 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'security' ? 'border-emerald-500 text-emerald-400' : 'border-transparent text-slate-400 hover:text-emerald-300'}`}
          >
            <ShieldAlert className="w-4 h-4" /> Seguridad (Zero Trust)
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-8 scroll-smooth">
          {journey.map((block) => {
            
            // 1. Bloque del Usuario
            if (block.type === 'user') {
              return (
                <div key={block.id} className="flex gap-4 justify-end">
                  <div className="max-w-2xl bg-indigo-600/90 text-white p-4 rounded-2xl rounded-tr-sm shadow-md border border-indigo-500">
                    <p className="text-sm font-medium leading-relaxed">{block.text}</p>
                  </div>
                </div>
              );
            }

            // 2. Bloque de Ruteo de GINI
            if (block.type === 'gini_routing') {
              const gini = SWARM_AGENTS.find(a => a.id === 'gini');
              return (
                <div key={block.id} className="flex gap-4 justify-start max-w-3xl">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 border border-fuchsia-500/30 ${gini.bg} ${gini.color}`}>
                    <gini.icon className="w-5 h-5" />
                  </div>
                  <div className="flex flex-col pt-1">
                    <span className="text-xs font-bold text-fuchsia-400 mb-1 flex items-center gap-1.5 uppercase tracking-wide">
                      {gini.name} <span className="text-slate-500 font-normal">| {gini.role}</span>
                    </span>
                    <div className="text-sm text-slate-300 bg-slate-900/50 p-3 rounded-lg border border-slate-800 border-l-2 border-l-fuchsia-500 shadow-sm">
                      {block.text}
                    </div>
                  </div>
                </div>
              );
            }

            // 3. ACTION CARD (El núcleo del trabajo del agente)
            if (block.type === 'action_card') {
              const agent = SWARM_AGENTS.find(a => a.id === block.agentId);
              const isProcessing = block.status === 'processing';
              const isExecuting = block.status === 'executing';
              const isDeployed = block.status === 'deployed';

              return (
                <div key={block.id} className="flex gap-4 justify-start w-full">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 border border-slate-700 ${agent.bg} ${agent.color} relative`}>
                    <agent.icon className={`w-5 h-5 ${isProcessing ? 'animate-pulse' : ''}`} />
                    {isProcessing && (
                      <span className="absolute -top-1 -right-1 flex h-3 w-3">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                      </span>
                    )}
                  </div>
                  
                  <div className="flex-1 max-w-4xl flex flex-col">
                    <span className={`text-xs font-bold mb-2 flex items-center gap-2 uppercase tracking-wide ${agent.color}`}>
                      {agent.name} <span className="text-slate-500 font-normal">| {agent.role}</span>
                      {isProcessing && <span className="text-[10px] bg-emerald-500/10 border border-emerald-500/30 px-2 py-0.5 rounded-full text-emerald-400 flex items-center gap-1.5 shadow-[0_0_10px_rgba(16,185,129,0.2)]"><Loader2 className="w-3 h-3 animate-spin"/> Sintetizando...</span>}
                      {isDeployed && <span className="text-[10px] bg-indigo-500/10 border border-indigo-500/30 px-2 py-0.5 rounded-full text-indigo-400 flex items-center gap-1.5"><CheckSquare className="w-3 h-3"/> En Producción</span>}
                    </span>

                    <div className="bg-[#111827] border border-slate-800/80 rounded-xl overflow-hidden shadow-lg flex flex-col transition-all duration-300">
                      
                      {/* ESTADO 1: Procesando Asíncronamente (SKELETON ANIMATION) */}
                      {isProcessing ? (
                        <div className="p-6 flex flex-col gap-4">
                          <div className="flex items-center gap-3 text-slate-400 border-b border-slate-800 pb-4">
                            <Cpu className="w-5 h-5 animate-pulse text-emerald-500/70" />
                            <span className="text-sm font-medium">{block.text}</span>
                          </div>
                          {/* Skeleton UI */}
                          <div className="space-y-3 mt-2">
                            <div className="h-4 bg-slate-800/50 rounded-md w-3/4 animate-pulse"></div>
                            <div className="h-4 bg-slate-800/50 rounded-md w-full animate-pulse delay-75"></div>
                            <div className="h-4 bg-slate-800/50 rounded-md w-5/6 animate-pulse delay-150"></div>
                          </div>
                          <div className="mt-4 h-24 bg-[#090C15] rounded-lg border border-slate-800/50 animate-pulse flex flex-col justify-center px-4">
                             <div className="h-3 bg-slate-800/70 rounded w-1/4 mb-3"></div>
                             <div className="h-3 bg-slate-800/70 rounded w-1/2"></div>
                          </div>
                        </div>
                      ) : (
                        /* ESTADOS 2 y 3: Tarea Completada o Ejecutando */
                        <>
                          <div className="bg-amber-500/10 border-b border-amber-500/20 p-4 flex gap-3 items-start">
                            <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                            <div>
                              <h4 className="text-xs font-bold text-amber-500 uppercase tracking-wider mb-1">Auto-Reflexión del Agente</h4>
                              <p className="text-sm text-amber-200/80 leading-relaxed">{block.reflection}</p>
                            </div>
                          </div>

                          <div className="p-5 border-b border-slate-800/80">
                            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Estrategia</h4>
                            <p className="text-sm text-slate-300 leading-relaxed">{block.strategy}</p>
                          </div>

                          <div className="p-4 bg-[#090C15] relative group">
                            <div className="text-xs font-mono text-slate-500 mb-2 select-none">// {agent.name}_output.jsx</div>
                            <pre className="text-sm font-mono text-emerald-300 overflow-x-auto p-2">
                              <code>{block.code}</code>
                            </pre>
                          </div>

                          {/* INTERACCIÓN: Human-in-the-Loop Controls o Terminal */}
                          {block.status === 'awaiting_approval' && (
                            <div className="p-4 bg-indigo-900/10 border-t border-indigo-500/20 flex items-center justify-between">
                              <div className="flex items-center gap-2 text-xs text-indigo-300 font-medium">
                                <TerminalSquare className="w-4 h-4 animate-pulse" /> Esperando autorización humana...
                              </div>
                              <div className="flex gap-3">
                                <button className="flex items-center gap-2 px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 rounded-md text-sm font-medium transition-colors">
                                  <X className="w-4 h-4" /> Rechazar
                                </button>
                                <button onClick={() => handleApprove(block.id)} className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-md text-sm font-medium shadow-[0_0_15px_rgba(16,185,129,0.3)] hover:shadow-[0_0_25px_rgba(16,185,129,0.5)] transition-all">
                                  <PlayCircle className="w-4 h-4" /> Aprobar e Inyectar
                                </button>
                              </div>
                            </div>
                          )}

                          {/* TERMINAL DE EJECUCIÓN (Aparece tras aprobar) */}
                          {(isExecuting || isDeployed) && (
                            <div className="p-4 bg-[#05080f] border-t border-slate-800">
                              <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
                                <span className="text-xs font-mono text-slate-500 flex items-center gap-2">
                                  <Terminal className="w-4 h-4" /> root@gini-v8:~# ejecución en local
                                </span>
                                {isExecuting ? (
                                  <span className="flex items-center gap-1.5 text-xs text-amber-500"><Loader2 className="w-3 h-3 animate-spin"/> Inyectando...</span>
                                ) : (
                                  <span className="flex items-center gap-1.5 text-xs text-emerald-500"><CheckCircle2 className="w-3 h-3"/> Despliegue Exitoso</span>
                                )}
                              </div>
                              <div className="font-mono text-xs space-y-1.5">
                                {block.terminalLogs?.map((log, i) => (
                                  <div key={i} className={`${log.includes('[EXITO]') ? 'text-emerald-400 font-bold' : log.includes('[OK]') ? 'text-slate-300' : 'text-slate-500'}`}>
                                    <span className="text-slate-600 mr-2">{'>'}</span>{log}
                                  </div>
                                ))}
                                {isExecuting && <div className="text-slate-500 animate-pulse"><span className="text-slate-600 mr-2">{'>'}</span>_</div>}
                              </div>
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  </div>
                </div>
              );
            }

            // 4. ALERTA DE AUTO-EVOLUCIÓN (Rotura de patrón visual)
            if (block.type === 'evo_alert') {
              return (
                <div key={block.id} className="flex justify-center w-full my-6">
                  <div className="w-full max-w-3xl bg-gradient-to-r from-orange-950/40 to-red-950/40 border border-orange-500/50 rounded-xl p-5 shadow-[0_0_30px_rgba(249,115,22,0.15)] relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-orange-500 to-red-500" />
                    
                    <div className="flex gap-4 items-start relative z-10">
                      <div className="w-12 h-12 rounded-full bg-orange-500/20 flex items-center justify-center shrink-0 border border-orange-500/50">
                        <AlertTriangle className="w-6 h-6 text-orange-500 animate-pulse" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-orange-500 font-bold text-lg mb-1 flex items-center gap-2">
                          ALERTA DE AUTO-EVOLUCIÓN <span className="text-xs bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded-full border border-orange-500/30">Requiere Acción</span>
                        </h3>
                        <p className="text-orange-200/80 text-sm leading-relaxed mb-4">
                          {block.text}
                        </p>
                        <div className="flex gap-3">
                          <button className="px-4 py-2 bg-orange-600 hover:bg-orange-500 text-white text-sm font-medium rounded-md shadow-[0_0_15px_rgba(234,88,12,0.4)] transition-all flex items-center gap-2 hover:-translate-y-0.5">
                            <Beaker className="w-4 h-4" /> Autorizar Mutación (Invocar a EVO)
                          </button>
                          <button className="px-4 py-2 bg-transparent hover:bg-white/5 text-orange-300 text-sm font-medium rounded-md border border-orange-500/30 transition-colors">
                            Ignorar y Continuar
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            }

            return null;
          })}
        </div>

        {/* ÁREA DE INPUT MEJORADA */}
        <div className="p-6 border-t border-slate-800/80 bg-[#111827] shadow-[0_-10px_30px_rgba(0,0,0,0.2)] z-20">
          <div className="max-w-4xl mx-auto relative flex items-center bg-[#0B0F19] border border-slate-700/80 rounded-xl focus-within:border-indigo-500/60 focus-within:ring-2 focus-within:ring-indigo-500/20 transition-all shadow-inner group">
            <div className="pl-4 text-slate-500 group-focus-within:text-indigo-400 transition-colors">
              <TerminalSquare className="w-5 h-5" />
            </div>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ingresa un requerimiento arquitectónico. Gini enrutará a los especialistas..."
              className="w-full bg-transparent border-none py-4 px-3 text-sm text-slate-200 placeholder-slate-600 focus:outline-none resize-none h-14"
            />
            <div className="pr-2 flex gap-2">
              <button className="p-2.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-white transition-all shadow-md hover:shadow-[0_0_15px_rgba(79,70,229,0.4)]">
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
          <div className="text-center mt-3 text-[11px] text-slate-500 font-medium tracking-wide flex items-center justify-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
            Gini en línea. Enjambre listo para orquestación paralela.
          </div>
        </div>
      </main>

      {/* PANEL DERECHO: Telemetría */}
      <aside className="w-72 bg-[#111827] border-l border-slate-800/60 flex flex-col shadow-2xl z-20">
        <div className="p-5 border-b border-slate-800/60 flex items-center justify-between">
          <h3 className="text-white font-bold text-sm flex items-center gap-2">
            <Activity className="w-4 h-4 text-indigo-500" />
            Telemetría del Enjambre
          </h3>
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
        </div>

        <div className="p-4 flex-1 overflow-y-auto space-y-3">
          {SWARM_AGENTS.map((agent) => (
            <div key={agent.id} className="bg-[#0B0F19] border border-slate-800/80 rounded-lg p-3 transition-colors hover:border-slate-700">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2.5">
                  <div className={`w-2 h-2 rounded-full shadow-sm ${
                    agent.status === 'working' ? 'bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.6)]' : 
                    agent.status === 'processing' ? 'bg-emerald-400 animate-ping' :
                    agent.status === 'waiting' ? 'bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.6)]' : 
                    agent.status === 'error' ? 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]' :
                    agent.status === 'completed' ? 'bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.6)]' :
                    'bg-slate-600'
                  }`} />
                  <span className="text-sm font-semibold text-slate-200">{agent.name}</span>
                </div>
                <span className={`text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-sm border ${agent.color.replace('text', 'border').replace('400', '500/30')} ${agent.bg} ${agent.color}`}>
                  {agent.role}
                </span>
              </div>
              
              <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-2 font-medium">
                {agent.status === 'processing' && <span className="text-emerald-400 flex items-center gap-1"><Cpu className="w-3 h-3 animate-pulse"/> Sintetizando...</span>}
                {agent.status === 'working' && <span className="text-emerald-400 flex items-center gap-1"><Activity className="w-3 h-3"/> Ejecutando hilos...</span>}
                {agent.status === 'waiting' && <span className="text-amber-400 flex items-center gap-1"><Clock className="w-3 h-3"/> Esperando dependencias</span>}
                {agent.status === 'error' && <span className="text-red-400 flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> Fallo cognitivo</span>}
                {agent.status === 'completed' && <span className="text-indigo-400 flex items-center gap-1"><Check className="w-3 h-3"/> Tarea finalizada</span>}
                {agent.status === 'idle' && <span className="text-slate-500 flex items-center gap-1"><Code2 className="w-3 h-3"/> Standby</span>}
              </div>
            </div>
          ))}
        </div>
      </aside>

    </div>
  );
}
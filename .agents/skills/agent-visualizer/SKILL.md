---
name: agent-visualizer
description: Analyzes the current local agent repository, generates or updates the agent_graph.json architecture mapping, and serves the interactive D3 web visualizer.
---

# Agent Architecture Visualizer Skill

This skill allows coding agents to inspect the developer's local agent codebase, map out agents, tools, models, workflows, and datastores into a structured schema, and serve an interactive D3 graph visualization.

---

## 🎯 When to Use This Skill

Activate this skill whenever the user:
- Asks to "visualize my agents", "show the architecture", "map out the project", or "update the agent diagram".
- Adds, refactors, or deletes an agent (`agents/*.py`), tool (`tools/*.py`), or workflow (`workflows/*.py`) and wants the documentation or architecture view refreshed.
- Wants an interactive way to inspect how their agents, tools, and local models connect.

---

## 📋 Architecture & Data Contract

The visualizer consumes a single JSON file:
```
tools/visualizer/agent_graph.json
```

This file MUST adhere to the schema defined in:
```
tools/visualizer/agent_graph.schema.json
```

### Node Types:
- `agent`: A LangGraph or autonomous state machine (e.g. `agents/base_agent.py`, `agents/gdrive_agent.py`).
- `tool`: A functional tool, API wrapper, or MCP server integration (e.g. `tools/gdrive_tool.py`).
- `workflow`: Multi-agent orchestration pipelines or diagnostic execution scripts (e.g. `scripts/setup_check.py`).
- `model`: A local LLM running in Ollama (e.g. `gemma2:9b`, `qwen2.5-coder:7b`).
- `datastore`: Local persistence engines (e.g. ChromaDB vector collections in `data/chroma_db`, SQLite databases).

### Edge Types:
- `calls`: An agent invoking a tool function.
- `uses_model`: An agent querying an Ollama model.
- `reads_writes`: An agent or tool interacting with a database or filesystem store.
- `orchestrates`: A workflow managing or sequencing agents.
- `depends_on`: A setup check or dependency link.

---

## 🔄 Workflow for the Agent

When requested to update or generate the visualizer:

### Step 1: Codebase Inspection
1. Read all files in `agents/`, `tools/`, `workflows/`, and `scripts/`.
2. For each agent:
   - Identify which model it invokes (`ChatOllama(model="...")` or `ollama.chat(...)`).
   - Identify the tools it imports or binds to (`TOOLS = { ... }` or `llm.bind_tools(...)`).
   - Note the state schema (`class AgentState(TypedDict)`).
3. For each tool:
   - Note the functions exported, external APIs called, and credential requirements.
4. For datastores:
   - Check if ChromaDB or SQLite is initialized in `data/`.

### Step 2: Update `tools/visualizer/agent_graph.json`
Write the updated nodes and edges into `tools/visualizer/agent_graph.json`.
- Provide a clear, concise `description`.
- Fill the `details` field with **rich Markdown** covering:
  - Architecture role
  - State schema / inputs and outputs
  - Tool signatures or model parameters
  - Safety constraints (e.g. read-only policies)

### Step 3: Serve the Visualizer
Instruct the user or launch the server with:

```bash
uv run python scripts/visualize.py
```

This starts Python's built-in `http.server` on `http://localhost:8080` (or next open port) and automatically opens the browser.

---

## 🛠️ Developer Customization
- **Webapp Location**: `tools/visualizer/index.html` (single file, zero npm/build steps).
- **Styling**: Uses custom CSS variables (`--color-agent`, `--color-tool`, etc.). ❌ Never use TailwindCSS or atomic CSS.
- **Dependencies**: D3.js and Marked.js loaded via CDN.

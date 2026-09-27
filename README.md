# 🤖 Local Agents Starter

> A lightweight, production-grade starting point for building, orchestrating, and running **100% local, sovereign AI agents** on your own machine.

Built with **[Ollama](https://ollama.com)**, **[LangGraph](https://github.com/langchain-ai/langgraph)**, **[uv](https://github.com/astral-sh/uv)**, and **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)**.

---

## ⚡ Why Local Agents?

- 🔒 **100% Data Sovereignty**: Your files, prompts, and personal data never leave your local hardware. No data is sent to external clouds or used to train third-party models.
- 💸 **Zero Subscription / API Fees**: Run unlimited inference tokens locally without worrying about API quotas, rate limits, or monthly credit card bills.
- 🚀 **Hardware Acceleration**: Takes full advantage of Apple Silicon Metal GPU acceleration and modern CPU/GPU architectures via Ollama.
- 🎯 **Deterministic Orchestration**: State-machine workflows powered by LangGraph ensure reliable tool calling, validation loops, and explicit termination.
- 🔌 **Standardized Tool Protocols**: Seamlessly connect local scripts, SQLite databases, ChromaDB vector stores, and MCP servers.

---

## 🛠️ The Tech Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Inference Engine** | **[Ollama](https://ollama.com)** | Local system daemon (`http://localhost:11434`) managing model weights and GPU acceleration |
| **Agent Orchestration** | **[LangGraph](https://github.com/langchain-ai/langgraph)** | Graph-based state machine for cyclical flows, branching, and deterministic agent logic |
| **Reasoning Model** | **[Google Gemma 2 (9B)](https://ollama.com/library/gemma2)** | Open-weights reasoning model for intent classification, synthesis, and planning |
| **Tool / Coding Model** | **[Qwen 2.5 Coder (7B)](https://ollama.com/library/qwen2.5-coder)** | Specialized open model for high-precision JSON tool calling and code execution |
| **Vector Memory** | **[ChromaDB](https://www.trychroma.com/)** | Lightweight, embedded local vector database for semantic search and retrieval |
| **Package Management** | **[uv](https://github.com/astral-sh/uv)** | Blazing-fast Python package resolver and virtual environment manager |
| **Tool Protocol** | **[MCP](https://modelcontextprotocol.io/)** | Open standard for connecting agents to tools, filesystems, and data sources |

---

## 📋 Prerequisites & System Requirements

### Hardware
- **macOS**: Apple Silicon (M1/M2/M3/M4) with **16GB+ unified memory** strongly recommended for running 7B–9B parameter models smoothly.
- **Linux / Windows**: Modern multi-core CPU with AVX support or dedicated NVIDIA/AMD GPU with 8GB+ VRAM.

### Software
1. **Git** (`git --version`)
2. **Python 3.10+** (managed automatically by `uv`)
3. **uv Package Manager**:
   ```bash
   curl -sSfL https://astral.sh/uv/install.sh | sh
   # or via Homebrew on macOS:
   # brew install uv
   ```
4. **Ollama Daemon**:
   - Download and install from [ollama.com](https://ollama.com) (or `brew install --cask ollama` on macOS).
   - Ensure Ollama is running (`ollama serve` or launch the Ollama application).

---

## 📦 How to Use This Starter

This repository is designed as a **self-contained starter template** rather than a collaborative package. You do not need to fork this repository or contribute upstream.

### 🌟 Option 1: GitHub Template (Recommended)
1. Click the green **"Use this template"** button at the top of the GitHub page ➔ select **"Create a new repository"**.
2. This creates a completely independent repository in your personal account with a clean initial commit and **zero fork linkages**, ensuring no accidental pull requests or upstream sync issues.

### 💻 Option 2: Clone & Reinitialize
If cloning via the terminal, clone into your new project directory and reinitialize Git to create your own clean root commit:
```bash
git clone https://github.com/<your-username>/local-agents-starter.git my-agent-workspace
cd my-agent-workspace
rm -rf .git && git init -b main
```

### 📁 Option 3: Download ZIP (No Git Required)
Click **Code ➔ Download ZIP** on GitHub and extract the folder to wherever you want to build your agents.

---

## 🚀 Quick Start (Under 2 Minutes)

### 1. Setup Workspace & Dependencies

Once you have your project directory set up:

```bash
cd local-agents-starter # or your project directory

# Install all dependencies and create virtual environment in ~1 second
uv sync
```

### 2. Pull Local Models

Pull the default recommended models via Ollama:

```bash
# General reasoning and agent planning (Google Gemma 2 - 9B)
ollama pull gemma2:9b

# Precision tool calling and code synthesis (Qwen 2.5 Coder - 7B)
ollama pull qwen2.5-coder:7b
```

### 3. Run Automated Diagnostics

Verify that your system binaries, Ollama daemon, model weights, and dependencies are ready:

```bash
uv run python scripts/setup_check.py
```

### 4. Run Your First Agent

Run the included baseline LangGraph agent:

```bash
uv run python agents/base_agent.py
```

You will see Gemma 2 reason through a prompt and stream its response 100% locally!

---

## 📁 Repository Structure

```
local-agents-starter/
├── README.md               # Quickstart guide & architectural overview
├── AGENTS.md               # Living operational instructions & conventions for AI agents
├── SETUP.md                # Dedicated step-by-step machine setup guide
├── pyproject.toml          # Project dependencies & CLI entrypoints
├── uv.lock                 # Deterministic dependency lockfile
│
├── agents/                 # Local agent state machine definitions
│   ├── base_agent.py       # Minimal starter LangGraph agent (Gemma 2:9b)
│   └── gdrive_agent.py     # Example tool-calling agent (Qwen 2.5 Coder)
│
├── tools/                  # Local tools, wrappers, and MCP connectors
│   └── gdrive_tool.py      # Example Google Drive API tool wrapper
│
├── workflows/              # Multi-agent orchestrations and batch scripts
├── config/                 # Environment configurations and prompt presets
├── data/                   # Local databases and ChromaDB vector store (gitignored)
├── scripts/                # Diagnostic scripts and setup automation
│   └── setup_check.py      # Automated setup verification tool
└── tests/                  # Verification test harnesses
    └── test_local_gemma.py # Direct Ollama inference smoke test
```

---

## 💡 How to Build Your Own Agent

Creating a new agent in this ecosystem is simple and boilerplate-free. Here is the blueprint (`agents/my_agent.py`):

```python
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# 2. Define Node Logic
def call_agent(state: AgentState):
    llm = ChatOllama(model="gemma2:9b", temperature=0.2)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build & Compile State Graph
def build_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_agent)
    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)
    return workflow.compile()

# 4. CLI Execution
if __name__ == "__main__":
    app = build_agent()
    result = app.invoke({"messages": [HumanMessage(content="Hello from my custom agent!")]})
    print(result["messages"][-1].content)
```

Run it with:
```bash
uv run python agents/my_agent.py
```

---

## 🔌 Optional Integrations: Google Drive

An example tool-calling agent is included in `agents/gdrive_agent.py` that demonstrates how to equip a local agent with search and read capabilities for Google Drive.

To enable it:
1. Download an OAuth 2.0 Desktop Client ID JSON from your Google Cloud Console and save it to `~/credentials.json`.
2. Run the one-time authentication flow:
   ```bash
   uv run python tools/gdrive_tool.py
   ```
3. Query Google Drive with your agent:
   ```bash
   uv run python agents/gdrive_agent.py "Search my Google Drive for recent notes"
   ```

---

## 🤖 Instructions for AI Coding Assistants

If you are working with an AI coding assistant (e.g. Antigravity, Claude Code, Cursor, Copilot Workspace), this repository contains an **[`AGENTS.md`](AGENTS.md)** file.

`AGENTS.md` is a living document that enforces:
- Strict single-command local CLI entrypoints (`agents/*.py`).
- No premature wrappers or unnecessary proxy abstractions.
- Deterministic LangGraph state machines.
- Clean separation of permissions and read-only external data policies.

Consult `AGENTS.md` before making architectural decisions or modifying agent workflows.

---

## 🔒 Maintenance & Contributions Policy

This repository is maintained strictly as an **independent starter foundation and reference template**.

- **No Upstream Contributions or Pull Requests**: To keep this starting point lightweight, unopinionated, and minimal, this project does not accept pull requests, feature requests, or external contributions.
- **Full Local Ownership**: You do not need to fork this project. Simply use GitHub's **"Use this template"** feature or clone/download the files to create your own repository. Once copied, it is 100% yours to customize, refactor, and build upon.

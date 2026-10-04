# Project Instructions & Agent Guidelines

Welcome to the **Local Agent Starter** project root. This repository serves as the central foundation for creating, orchestrating, and maintaining local AI agents, tools, workflows, and integrations on this machine.

---

## 🔄 Living Document Protocol

> **IMPORTANT**: `AGENTS.md` is a **living document**. It must evolve alongside the project to preserve context, design decisions, and operational standards across all current and future AI agent sessions.

### Rules for AI Agents:
1. **Active Suggestion**: Whenever a new feature, architecture decision, dependency, workflow pattern, or tool convention is introduced or modified during a conversation, the agent **MUST** review `AGENTS.md` and suggest necessary updates.
2. **Context Persistence**: Always capture critical instructions, code styles, and operational setup steps into `AGENTS.md` (or `.agents/` rules) so subsequent sessions automatically inherit them.
3. **Refinement & Pruning**: Keep sections clear, concise, and structured. Update outdated guidelines as the codebase evolves.
4. **Setup Guide Maintenance**: Whenever new dependencies, model requirements, environment variables, or tool prerequisites are introduced, the agent **MUST** keep [`SETUP.md`](SETUP.md) and [`scripts/setup_check.py`](scripts/setup_check.py) updated alongside `AGENTS.md`.

---

## 🎯 Project Goal & Vision

- **Local-First Agents**: Move away from exclusive reliance on cloud-hosted/deployed agent SaaS platforms by building, running, and managing local agents directly on the host machine.
- **Modular & Extensible**: Establish clean abstractions for agent roles, tool integrations (MCP servers, APIs, local scripts), and multi-agent coordination.
- **Reproducible & Managed**: Maintain a well-structured project layout with shared libraries, environment configurations, and execution scripts.

---

## 📁 Repository Layout & Organization (Target Standard)

As the project develops, code and configurations should follow this structure:

```
.
├── AGENTS.md                  # This living instruction & convention file
├── README.md                  # Public overview and quickstart guide
├── SETUP.md                   # Machine setup guide & diagnostics
├── .agents/                   # Workspace-specific agent rules, skills, and plugins
│   ├── rules/                 # Hierarchical contextual rules for agents
│   └── skills/                # On-demand custom workflow skills
├── agents/                    # Local agent definitions & core logic
├── tools/                     # Local tools, MCP servers, and API wrappers
├── workflows/                 # Multi-agent orchestrations and task scripts
├── config/                    # Environment, model, and system configurations
└── tests/                     # Test suites for agents, tools, and workflows
```

---

## 🛠️ Operational & Development Directives

### 1. Code Standards & Architecture
- **Primary Runtime & Environment**: **Python** (managed via `uv` for ultra-fast dependency resolution and virtual environments).
- **Secondary / Frontend Stack**: **TypeScript / Node.js** for web applications, dashboards, or browser extension tools.
- **Communication & Feedback Style**: **Direct, Objective, Un-pandering**. Provide matter-of-fact technical critique and trade-off analysis. Avoid sycophancy, excessive enthusiasm, or unearned validation. Focus strictly on technical correctness and engineering standards.
- **No Premature / Unnecessary Abstractions**: Do not build custom wrappers, middleman proxy classes, or generic helper frameworks over pre-built libraries (e.g. MCP adapters, LangGraph, SDKs). If standard usage is a few lines of code, write it directly. Avoid inventing custom abstraction layers that add failure points.
- **Common Agent Anti-Patterns to Avoid**:
  1. *Custom Prompt Engines*: Do not build custom template parsing frameworks when standard Python f-strings or Pydantic models suffice.
  2. *Custom DB Wrappers*: Do not write middleman classes around ChromaDB; call standard ChromaDB APIs directly.
  3. *Unstructured Chat Loops*: Avoid freeform "agent chats" without strict Pydantic schema validation and explicit LangGraph state machine termination.
  4. *Deep Directory Nesting*: Keep folder structures flat until concrete implementations warrant sub-packages.
  5. *Silent Fallbacks / Exception Swallowing*: Never return dummy strings or swallow errors silently; raise exceptions explicitly so failures are clear.
- **Domain-Specific Specialized Agents**: Build dedicated agents bound to specific domains, permissions, and account tokens rather than creating bloated, monolithic agents. This enforces least-privilege security and prevents cross-account credential pollution.
- **Single-Command Local Agent Entrypoints**: Every local agent (`agents/*.py`) must provide a clean, self-contained CLI entrypoint (via `argparse` or script runner) so that invoking the agent is always a single command line (e.g. `uv run python agents/gdrive_agent.py "Search recent files"`). All underlying operations—database queries, vector retrieval, qualification scoring, and tool execution—must run autonomously inside the script without requiring interactive terminal intervention.
- **Stop on Errors & Discuss Next Steps**: If an agent execution or command encounters an error, API failure, or unexpected behavior, **DO NOT** attempt automatic retry loops or run workaround shell scripts in chat. Immediately stop execution, report the error clearly to the user, and discuss next steps together.
- **Strict Action Boundaries (Files & Agent Execution Only)**: The assistant must ONLY edit code files and run official agent entrypoint scripts (`agents/*.py`). Never execute ad-hoc python shell snippets, manual SQL queries, or multi-step command chains in chat.
- **Data Sanity & Synthetic Data Filtering**: All data ingestion engines must run generic sanity filters to reject synthetic/fake AI placeholder data (e.g. `@example.com`, placeholder names, header row dumps). Strip raw trailing numbers, booleans, or CSV artifacts merged into text cells.
- **Type Safety & Clean Code**: Use explicit type annotations (e.g., Python `mypy`/`pydantic`, TypeScript strict mode), self-documenting signatures, and clean error handling.

### 2. UI & Frontend Guidelines (Strict Directives)
- ❌ **NEVER USE TAILWINDCSS OR ATOMIC CSS**: Do not install, generate, or import TailwindCSS or any utility-first atomic CSS framework under any circumstances.
- ✅ **Styling Preference**: Write standard custom **SCSS / CSS** for clean modular styles, or use **Material Design** components/guidelines (e.g., Material Design 3).
- ✅ **Angular State Management**: Use modern **Angular Signals** for reactive state. ❌ **Strictly forbid RxJS Observables (for state management) or any Redux variants (NgRx, Akita, Redux Toolkit)**.

### 3. Model Providers & Local Inference
- **Local Inference Engine**: **Ollama** running as a local system daemon (`http://localhost:11434`), taking full advantage of Apple Silicon Metal GPU acceleration.
- **Primary Focus**: **100% Local Compute**. No required subscriptions or external APIs.
- **Recommended Open Models**:
  - **Gemma 2** (`gemma2:9b`): Google's open-weights model family for general reasoning and agent execution.
  - **Qwen 2.5 Coder** (`qwen2.5-coder:7b` / `14b`): Specialized open model for coding tasks and high-accuracy tool calling.

### 4. Architecture & Standard Frameworks
- **Tool Protocol**: **MCP (Model Context Protocol)** using the official `mcp` Python SDK over Stdio/SSE.
- **Agent Orchestration**: **LangGraph** for stateful, graph-based agent workflows, persistence, and deterministic execution loops.
- **Local Vector Memory**: **ChromaDB** is the primary default for local vector memory due to its established ecosystem standard status. **LanceDB** (Apache Arrow backed) is the designated performance fallback if high-scale memory/VRAM constraints arise.

### 5. Community Alignment & Tooling Health Audits
- **Mainstream Standards Priority**: Favor battle-tested, broadly-adopted foundations with strong community and enterprise backing (e.g. PyPA standards, official SDKs, MCP, LangGraph, Pydantic, ChromaDB). Avoid niche, transient, or unmaintained libraries.
- **Continuous Alignment Audits**: Periodically evaluate the toolchain and dependencies to ensure the project stays aligned with evolving mainstream agent conventions and does not drift into obsolete custom abstractions.

### 6. Execution & Safety Guidelines
- **Strict Read-Only Source Data Policy**: All source files, forms, spreadsheets, and documents in external storage (e.g., Google Drive) are strictly **READ-ONLY**. Agents must **NEVER** edit, modify, overwrite, or delete source files. All deduplication and indexing occur locally, and reports are written to **brand-new output files**.
- **Command Execution & File Edit Rationale**: Whenever proposing or executing shell commands or modifying files, output a concise **1-sentence technical rationale focusing on WHY the action is taking place** (the root objective or diagnostic reason) rather than simply describing WHAT the command does. This gives the user clear visibility into system behavior and underlying context before any action occurs.
- **Local Verification**: Always test and run code locally using standard test commands before declaring tasks complete.
- **Empirical Debugging**: Base bug fixes strictly on un-truncated logs and execution output. Never mask errors or swallow exceptions silently.
- **Sandboxed Command Execution**: Execute shell commands using project-relative paths, respecting local environment configurations.

### 7. Agent Interaction Workflow
- **Planning**: For complex features or multi-step architecture changes, create an implementation plan before writing code.
- **Walkthroughs**: Record key changes, test results, and visual evidence (if applicable) in walkthrough artifacts upon completion.
- **Continuous Documentation**: Update `AGENTS.md` whenever new agent structures or standards are finalized.

---

## 📋 Agent & Tool Catalog (Living Registry)

*(As local agents and tools are built, list and summarize them here for easy discovery.)*

| Agent / Tool | Location | Description | Status |
| :--- | :--- | :--- | :--- |
| **Setup Diagnostic Tool** | [`scripts/setup_check.py`](scripts/setup_check.py) | Automated environment, Ollama, model, dependency, and OAuth diagnostic tool | ✅ Verified |
| **Local Gemma Harness** | [`tests/test_local_gemma.py`](tests/test_local_gemma.py) | Verification test harness for local inference with Google Gemma 2 (9B) via Ollama | ✅ Verified |
| **LangGraph Base Agent** | [`agents/base_agent.py`](agents/base_agent.py) | Deterministic LangGraph state machine powered by local Gemma 2 (9B) | ✅ Verified |
| **Google Drive Tooling** | [`tools/gdrive_tool.py`](tools/gdrive_tool.py) | Google Drive API integration for search, read, create, and update operations | ✅ Verified |
| **Google Drive Agent** | [`agents/gdrive_agent.py`](agents/gdrive_agent.py) | Local LangGraph agent powered by Qwen 2.5 Coder for natural language Drive management | ✅ Verified |
| **Agent Architecture Visualizer** | [`tools/visualizer/index.html`](tools/visualizer/index.html) | Standalone D3.js interactive architecture graph & Markdown inspector webapp | ✅ Verified |
| **Visualizer Runner Script** | [`scripts/visualize.py`](scripts/visualize.py) | Single-command Python HTTP server and workspace scanner for the visualizer | ✅ Verified |
| **Visualizer Agent Skill** | [`.agents/skills/agent-visualizer/SKILL.md`](.agents/skills/agent-visualizer/SKILL.md) | Agent skill for generating architecture schemas and serving visualizations | ✅ Verified |

---

*Last Updated: 2026-10-04 (Agent Architecture Visualizer Added)*

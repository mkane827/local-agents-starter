# Agent Architecture Rules: True LLM Cognitive Core Requirement

## 1. No Pseudo-Agents or Heuristic Keyword Facades
- **Strict Prohibition**: Never build hardcoded Python `if/else` keyword-matching scripts and label them as "agents", or wrap procedural scripts in cosmetic LangGraph nodes.
- **Mandatory LLM Core**: Every agent defined in `agents/*.py` MUST be driven by a real local LLM cognitive core running on host Ollama (e.g. `qwen2.5-coder:7b`, `gemma2:9b`).
- **Agent Responsibilities**: The LLM must be responsible for:
  1. Interpreting ambiguous natural language instructions.
  2. Reasoning through task decomposition and planning.
  3. Generating structured tool calls or execution parameters.
  4. Evaluating outcome audits, critic feedback, and errors to decide next steps.

## 2. Strict Division of Labor: Agents vs. Tools
- **Tools (`tools/*.py`)**: Deterministic execution engines (e.g. math operations, transforms, database queries, API requests). Tools perform operations; they do not make autonomous decisions.
- **Agents (`agents/*.py`)**: Intelligent operators that command tools via LangGraph state machines driven by local LLM reasoning.

## 3. No Silent Degradation to Hardcoded Fallbacks
- An agent must never silently substitute model reasoning with rigid string matching to bypass connectivity or sandbox obstacles.
- If a model call fails or encounters an environment blocker, surface the error transparently rather than faking agent behavior with procedural logic.

# 🚀 Local Agent Starter — Machine Setup Guide

This guide walks you through setting up and running 100% local, sovereign AI agents on your machine in **3 simple steps**.

---

## 🔍 Automated Diagnostic Check

To check what is currently installed and what is missing on your machine at any time, run:

```bash
uv run python scripts/setup_check.py
```

This diagnostic script automatically verifies your Python version, `uv` package manager, Ollama server daemon, local model weights (`gemma2:9b`, `qwen2.5-coder:7b`), and dependencies.

---

## 🛠️ 3-Step Setup Instructions

### Step 1: Clone Repository & Install Dependencies

If you haven't installed `uv` yet, install it in one command:
```bash
curl -sSfL https://astral.sh/uv/install.sh | sh
# or on macOS with Homebrew:
# brew install uv
```

Clone the repository and install all dependencies:
```bash
git clone https://github.com/<your-username>/local-agents-starter.git
cd local-agents-starter

# Install dependencies and create a dedicated virtual environment in 1 second
uv sync
```

---

### Step 2: Install Ollama & Pull Open Models

1. Download and run **Ollama for Mac/Linux/Windows** from [ollama.com](https://ollama.com) (or `brew install --cask ollama` on macOS).
2. Pull the recommended open models:

```bash
# 1. Reasoning & general agent execution (Google Gemma 2 - 9B)
ollama pull gemma2:9b

# 2. Fast code synthesis & tool calling (Qwen 2.5 Coder - 7B)
ollama pull qwen2.5-coder:7b
```

---

### Step 3: Run Your First Local Agent

Test that your local LangGraph state machine and Ollama inference are working together:

```bash
uv run python agents/base_agent.py
```

You should see a streamed response generated 100% locally by Gemma 2 on your machine with zero cloud API dependencies!

---

## 🔌 Optional: Google Drive Tool Integration

If you want your local agent to search, read, and create documents in Google Drive:

1. Create a Google Cloud project with Google Drive API enabled, and download your **OAuth 2.0 Client ID (Desktop)** JSON.
2. Save the file to `~/credentials.json`.
3. Complete the one-time browser authentication:
   ```bash
   uv run python tools/gdrive_tool.py
   ```
4. Run the Google Drive agent:
   ```bash
   uv run python agents/gdrive_agent.py "Search my Google Drive for recent notes"
   ```

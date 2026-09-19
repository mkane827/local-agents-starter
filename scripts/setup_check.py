"""
Automated Setup Verification Script for Local Agent Starter.
Checks core prerequisites (Python, Git, uv, Ollama daemon, local models, LangGraph dependencies)
and reports optional tool integrations (Google Drive OAuth).
"""
import sys
import os
import shutil
import urllib.request
import json

def print_row(status: str, component: str, info: str):
    print(f"{status:8} | {component:32} | {info}")

def check_core_step(name: str, condition: bool, pass_info: str, fail_info: str) -> bool:
    status = "✅ PASS" if condition else "❌ FAIL"
    info = pass_info if condition else fail_info
    print_row(status, name, info)
    return condition

def check_optional_step(name: str, condition: bool, pass_info: str, missing_info: str) -> bool:
    status = "✅ READY" if condition else "ℹ️ OPTIONAL"
    info = pass_info if condition else missing_info
    print_row(status, name, info)
    return condition

def run_diagnostics():
    print("\n🔍 Local Agent Starter — Machine Setup Diagnostics")
    print("=" * 80)
    print(f"{'STATUS':8} | {'COMPONENT':32} | {'DETAILS'}")
    print("-" * 80)

    core_passed = True

    # 1. Check Python Version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 10)
    core_passed &= check_core_step("Python Runtime", py_ok, f"Python {py_ver}", f"Python {py_ver} (Requires >= 3.10)")

    # 2. Check Git CLI
    git_path = shutil.which("git")
    core_passed &= check_core_step("Git CLI", git_path is not None, git_path or "", "Missing -> Run: xcode-select --install")

    # 3. Check uv Binary
    uv_path = shutil.which("uv") or os.path.expanduser("~/.local/bin/uv")
    uv_installed = os.path.exists(uv_path) or shutil.which("uv") is not None
    core_passed &= check_core_step("uv CLI Binary", uv_installed, uv_path if uv_installed else "", "Missing -> Run: curl -sSfL https://astral.sh/uv/install.sh | sh")

    # 4. Check Ollama CLI Binary
    ollama_bin = shutil.which("ollama") or "/usr/local/bin/ollama"
    ollama_installed = os.path.exists(ollama_bin) or shutil.which("ollama") is not None
    core_passed &= check_core_step("Ollama CLI Binary", ollama_installed, ollama_bin if ollama_installed else "", "Missing -> Install from https://ollama.com")

    # 5. Check Ollama Daemon HTTP Endpoint
    ollama_running = False
    try:
        req = urllib.request.urlopen("http://127.0.0.1:11434/", timeout=2)
        ollama_running = req.getcode() == 200
    except Exception:
        pass
    core_passed &= check_core_step("Ollama Daemon", ollama_running, "http://127.0.0.1:11434 (Active)", "Not running -> Run 'ollama serve' or open Ollama app")

    # 6. Check Installed Models in Ollama
    models = []
    if ollama_running:
        try:
            req = urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3)
            data = json.loads(req.read().decode())
            models = [m.get("name", "") for m in data.get("models", [])]
        except Exception:
            pass

    gemma_present = any("gemma2:9b" in m for m in models)
    qwen_present = any("qwen2.5-coder:7b" in m for m in models)
    core_passed &= check_core_step("Reasoning Model (Gemma 2)", gemma_present, "gemma2:9b (Installed)", "Missing -> Run: ollama pull gemma2:9b")
    core_passed &= check_core_step("Tool Model (Qwen 2.5 Coder)", qwen_present, "qwen2.5-coder:7b (Installed)", "Missing -> Run: ollama pull qwen2.5-coder:7b")

    # 7. Check Core Python Dependencies
    core_packages = ["langgraph", "chromadb", "ollama", "mcp", "langchain", "langchain_ollama"]
    missing_core = []
    for pkg in core_packages:
        try:
            __import__(pkg)
        except ImportError:
            missing_core.append(pkg)
    core_passed &= check_core_step("Core Python Packages", len(missing_core) == 0, "All core packages installed", f"Missing: {', '.join(missing_core)} -> Run: uv sync")

    print("-" * 80)
    print("Optional Tool Integrations:")
    print("-" * 80)

    # 8. Optional Google Drive Tool Check
    creds_path = os.path.expanduser("~/credentials.json")
    token_path = os.path.expanduser("~/.gdrive_token.json")
    check_optional_step("Google Drive Credentials", os.path.exists(creds_path), f"Found at {creds_path}", "Not configured -> Place OAuth JSON at ~/credentials.json (if using Drive agent)")
    check_optional_step("Google Drive OAuth Token", os.path.exists(token_path), f"Found at {token_path}", "Not authenticated -> Run: uv run python tools/gdrive_tool.py (if using Drive agent)")

    print("=" * 80)
    if core_passed:
        print("🎉 All core local agent prerequisites are satisfied! You are ready to build and run local agents.\n")
    else:
        print("⚠️ Some core prerequisites are missing. Please follow the recommendations above before running agents.\n")

if __name__ == "__main__":
    run_diagnostics()

"""
Local Agent Architecture Visualizer Server.
Serves the self-contained D3 web application using Python's built-in http.server.
Usage:
    uv run python scripts/visualize.py
    uv run python scripts/visualize.py --port 8080 --no-browser
"""
import sys
import os
import argparse
import webbrowser
import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

VISUALIZER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "visualizer")
DATA_FILE = os.path.join(VISUALIZER_DIR, "agent_graph.json")

def find_available_port(start_port: int = 8080, max_attempts: int = 20) -> int:
    """Finds the first available TCP port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port

class VisualizerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=VISUALIZER_DIR, **kwargs)

    def log_message(self, format, *args):
        # Keep server terminal output clean and non-intrusive
        if args and str(args[1]) in ['404', '500']:
            sys.stderr.write(f"⚠️  Visualizer HTTP Warning: {format % args}\n")

def scan_and_sync_workspace(project_root: str):
    """Inspects agents/, tools/, and workflows/ to ensure all local files appear in agent_graph.json."""
    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return

    existing_files = {n.get("file") for n in data.get("nodes", []) if n.get("file")}
    updated = False

    # Scan agents/
    agents_dir = os.path.join(project_root, "agents")
    if os.path.exists(agents_dir):
        for f in os.listdir(agents_dir):
            if f.endswith(".py") and not f.startswith("__"):
                rel_path = f"agents/{f}"
                if rel_path not in existing_files:
                    name = f.replace(".py", "").replace("_", " ").title()
                    data["nodes"].append({
                        "id": f"agent-{f.replace('.py', '').replace('_', '-')}",
                        "name": f"{name} Agent",
                        "type": "agent",
                        "description": f"Local agent defined in {rel_path}.",
                        "file": rel_path,
                        "details": f"### {name} Agent\nDefined in `{rel_path}`.",
                        "status": "active",
                        "tags": ["agent", "local"]
                    })
                    updated = True

    # Scan tools/
    tools_dir = os.path.join(project_root, "tools")
    if os.path.exists(tools_dir):
        for f in os.listdir(tools_dir):
            if f.endswith(".py") and not f.startswith("__"):
                rel_path = f"tools/{f}"
                if rel_path not in existing_files:
                    name = f.replace(".py", "").replace("_", " ").title()
                    data["nodes"].append({
                        "id": f"tool-{f.replace('.py', '').replace('_', '-')}",
                        "name": f"{name} Tool",
                        "type": "tool",
                        "description": f"Local tool defined in {rel_path}.",
                        "file": rel_path,
                        "details": f"### {name} Tool\nDefined in `{rel_path}`.",
                        "status": "active",
                        "tags": ["tool", "local"]
                    })
                    updated = True

    if updated:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("🔄 Updated tools/visualizer/agent_graph.json with newly discovered workspace files.")

def main():
    parser = argparse.ArgumentParser(description="Serve the local Agent Architecture Visualizer.")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    parser.add_argument("--no-scan", action="store_true", help="Skip scanning the workspace for new agents/tools")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if not args.no_scan:
        scan_and_sync_workspace(project_root)

    port = find_available_port(args.port)
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, VisualizerHandler)

    url = f"http://localhost:{port}"
    print("\n" + "=" * 65)
    print("⚡ Local Agent Architecture Visualizer")
    print("=" * 65)
    print(f"📡 Serving visualizer at: {url}")
    print("💡 Click nodes in the graph to inspect detailed Markdown specs.")
    print("🛑 Press Ctrl+C to stop the server.")
    print("=" * 65 + "\n")

    if not args.no_browser:
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Visualizer server stopped.")
        httpd.server_close()

if __name__ == "__main__":
    main()

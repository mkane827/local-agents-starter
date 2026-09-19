"""
Google Drive Agent powered by local Ollama models (Qwen 2.5 Coder / Gemma 2) and LangGraph.
Allows natural language searching, reading, synthesizing, and creating files in Google Drive.
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from tools.gdrive_tool import search_drive_files, read_drive_file, create_drive_file, update_drive_file

# 1. State Schema
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# 2. Tool Directory
TOOLS = {
    "gdrive_search": search_drive_files,
    "gdrive_read": read_drive_file,
    "gdrive_create": create_drive_file,
    "gdrive_update": update_drive_file
}

SYSTEM_PROMPT = """You are an intelligent Google Drive Assistant running 100% locally.
You have access to the following tools:
- gdrive_search(query: str): Search files in Google Drive.
- gdrive_read(file_id: str): Read text content of a file by its ID.
- gdrive_create(name: str, content: str): Create a new document in Google Drive.
- gdrive_update(file_id: str, new_content: str): Update/append text content in a Google Drive file by ID.

To call a tool, output ONLY a JSON block formatted like this:
{"name": "gdrive_update", "arguments": {"file_id": "123", "new_content": "GOTCHA"}}

When you have the final answer, provide a clear, helpful response in natural language.
"""

def call_model_node(state: AgentState):
    llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.1)
    messages = [HumanMessage(content=SYSTEM_PROMPT)] + list(state["messages"])
    response = llm.invoke(messages)
    return {"messages": [response]}

def clean_json_str(content: str) -> str:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 2:
            cleaned = "\n".join(lines[1:-1]).strip()
    return cleaned

def call_tools_node(state: AgentState):
    last_msg = state["messages"][-1]
    content = clean_json_str(last_msg.content)
    
    try:
        data = json.loads(content)
        tool_name = data.get("name")
        args = data.get("arguments", {})
        
        if tool_name in TOOLS:
            print(f"\n🛠️ Executing Google Drive Tool: {tool_name} with args: {args}")
            tool_func = TOOLS[tool_name]
            result = tool_func(**args)
            print(f"📄 Tool Result Received ({len(result)} bytes)")
            return {"messages": [ToolMessage(content=result, tool_call_id=tool_name)]}
    except Exception as e:
        print(f"Error parsing tool call: {e}")
        
    return {"messages": []}

def should_continue(state: AgentState):
    last_msg = state["messages"][-1]
    content = clean_json_str(last_msg.content)
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "name" in data and "arguments" in data:
            return "tools"
    except Exception:
        pass
    return END

def build_gdrive_agent_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model_node)
    workflow.add_node("tools", call_tools_node)
    
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

def run_gdrive_agent(prompt: str):
    print(f"\n📂 User Request: '{prompt}'")
    print("=" * 60)
    app = build_gdrive_agent_graph()
    result = app.invoke({"messages": [HumanMessage(content=prompt)]})
    
    final_response = result["messages"][-1].content
    print("\n🤖 Local Drive Agent Final Response:")
    print("-" * 60)
    print(final_response)
    print("-" * 60)

if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Search my Google Drive for recent project notes or documents."
    run_gdrive_agent(task)

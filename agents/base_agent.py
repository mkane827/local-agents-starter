"""
Base Local LangGraph Agent using Ollama (Gemma 2:9b) and standard tool architecture.
"""
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 1. Define Agent State Schema
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# 2. Initialize Local Model (Gemma 2:9b via Ollama)
def get_local_llm(model_name: str = "gemma2:9b") -> ChatOllama:
    return ChatOllama(
        model=model_name,
        temperature=0.2,
    )

# 3. Define Graph Nodes
def call_agent_node(state: AgentState):
    llm = get_local_llm()
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 4. Build LangGraph Workflow
def build_local_agent_graph():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("agent", call_agent_node)
    
    # Add Edges
    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)
    
    # Compile State Machine
    return workflow.compile()

if __name__ == "__main__":
    app = build_local_agent_graph()
    result = app.invoke({"messages": [HumanMessage(content="Explain why local AI agents are powerful in 2 bullet points.")]})
    
    print("🤖 Local LangGraph Agent Response:")
    print("=" * 60)
    for msg in result["messages"]:
        if msg.type == "ai":
            print(msg.content)
    print("=" * 60)

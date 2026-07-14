from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from context_schema import AgentState
from ai_engine import llm_engine
from tools import tools_list
from persona import system_message

def agent_node(state: AgentState):
    # Seed the analyst persona for the LLM call without storing it in the
    # accumulating message history, so every entrypoint gets the same agent.
    messages = [system_message()] + state["messages"]
    response = llm_engine.invoke(messages)
    return {"messages": [response]}

# --- NODE 2: The Tool Executor ---
tool_node = ToolNode(tools_list)

# --- LOGIC: Should we continue? ---
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# --- GRAPH CONSTRUCTION ---
def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent") # Loop back to agent to explain results

    return workflow.compile()
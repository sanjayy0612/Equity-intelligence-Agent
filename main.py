from langchain_core.messages import HumanMessage
from states import build_graph
import sys

# 1. Initialize the Graph
try:
    app = build_graph()
    print("🚀 OpenFinAgent Initialized (Llama 3.1 + OpenBB + LangGraph)")
    print("✅ Local Inference: Connected to Ollama (localhost)")
    print("👉 Type 'quit' to exit.\n")
except Exception as e:
    print(f"❌ Critical Error: Could not build graph. Check states.py or ai_engine.py.\nError: {e}")
    sys.exit(1)

# The analyst persona now lives in persona.py and is seeded by the graph, so both
# this CLI and the Streamlit app (app.py) talk to the same agent.

# 2. Main Execution Loop
while True:
    try:
        # Get User Input
        user_input = input("User: ").strip()
        
        # Handle empty input
        if not user_input:
            continue
            
        # Handle quit commands
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye! 👋")
            break
        
        # Prepare initial state (the persona is seeded by the graph)
        initial_state = {
            "messages": [
                HumanMessage(content=user_input)
            ]
        }
        
        # 3. Stream the Graph
        for event in app.stream(initial_state):
            for node_name, node_state in event.items():
                last_message = node_state["messages"][-1]
                
                # --- CASE 1: The Agent Node Just Finished ---
                if node_name == "agent":
                    # Check if the agent wants to use a tool
                    if last_message.tool_calls:
                        # It wants to use a tool!
                        tool_names = [t["name"] for t in last_message.tool_calls]
                        print(f"   🤖 Agent (Thought): I need more data. Calling tool: {tool_names}...")
                    else:
                        # It has a final answer
                        print(f"   🤖 Agent (Answer): {last_message.content}")

                # --- CASE 2: The Tool Node Just Finished ---
                elif node_name == "tools":
                    # The tool ran successfully and returned data
                    print("   ⚙️  System: Data fetched successfully.")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("   Please try again or type 'quit' to exit.")
        # Don't break - allow user to continue after non-critical errors
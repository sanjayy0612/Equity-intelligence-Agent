import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from states import build_graph

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="OpenFinAgent", 
    page_icon="📈",
    layout="centered"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stStatus {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 OpenFinAgent")
st.markdown("### The AI Financial Analyst powered by OpenBB & Llama 3.1")
st.caption("Capabilities: Real-time Stock Data, Fundamental Analysis, Sector Comparisons")

# --- 2. SESSION STATE SETUP ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the Graph (Cache it so we don't rebuild it on every click)
@st.cache_resource
def get_app():
    return build_graph()

app = get_app()

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("**Active Tools:**")
    st.markdown("- `fundamental_analysis`")
    st.markdown("- `get_stock_price`")
    st.markdown("- `get_company_profile`")
    st.markdown("- `stock_name`")

# --- 4. DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- 5. HANDLE USER INPUT ---
if user_input := st.chat_input("Ask about stocks (e.g., 'Analyze Tesla's profitability')"):
    
    # A. Display User Message
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # B. Run the Agent
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # We need to construct the input state with the FULL history
        # This allows the agent to remember context from previous turns
        inputs = {"messages": st.session_state.messages}

        # Status container to show "Thinking..."
        with st.status("🧠 Agent is thinking...", expanded=True) as status:
            
            # Run the graph stream
            try:
                final_response_content = ""
                
                for event in app.stream(inputs):
                    for node_name, node_state in event.items():
                        
                        # Get the latest message from this node
                        last_msg = node_state["messages"][-1]
                        
                        # --- CASE 1: Agent Decides to Call a Tool ---
                        if node_name == "agent" and last_msg.tool_calls:
                            tool_names = [t["name"] for t in last_msg.tool_calls]
                            status.write(f"🔍 **Decided to call:** `{', '.join(tool_names)}`")
                            # status.update(label=f"Calling {tool_names}...", state="running")
                        
                        # --- CASE 2: Tool Execution Finished ---
                        elif node_name == "tools":
                            # The tool output is usually a ToolMessage
                            # We can show a small checkmark
                            status.write("✅ **Tool execution complete.** Processing data...")
                        
                        # --- CASE 3: Final Answer ---
                        elif node_name == "agent" and not last_msg.tool_calls:
                            final_response_content = last_msg.content
                
                # Update status to complete
                status.update(label="Response Ready", state="complete", expanded=False)
                
                # Display Final Answer
                if final_response_content:
                    message_placeholder.markdown(final_response_content)
                    # Save to history
                    st.session_state.messages.append(AIMessage(content=final_response_content))
                else:
                    st.error("⚠️ The agent did not produce a final response.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
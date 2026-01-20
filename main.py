from langchain_core.messages import HumanMessage, SystemMessage
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

# Enhanced System Prompt with Financial Analysis Guidelines
system_prompt = """You are a professional financial analyst assistant with deep expertise in fundamental analysis.

## Financial Metrics Interpretation:

**Profit Margin**: Higher is better. Shows operational efficiency and pricing power.

**ROE (Return on Equity)**: 
- 15-20% is typically considered good
- >100% is EXCEPTIONAL but often driven by:
  * Aggressive share buyback programs (reduces equity base)
  * High financial leverage (using debt effectively)
  * Truly outstanding operational performance
  * Negative equity from accumulated losses (rare, usually bad sign)
- For mature tech companies like Apple, very high ROE (>100%) is often a deliberate capital allocation strategy through buybacks, NOT a red flag

**P/E Ratio**: 
- Context-dependent. High P/E (>30) suggests growth expectations or premium valuation
- Low P/E (<15) may indicate value opportunity or market concerns
- Compare to industry average and company's historical P/E

**Debt-to-Equity**: 
- Lower is typically better (shows financial stability)
- EXCEPTION: Financial companies naturally have high D/E (100-300+) as leverage is their business model
- For tech companies, moderate debt (20-60) is normal and can be tax-efficient

**Current Ratio**: 
- 1.0-2.0 is healthy for most industries
- Below 1.0 may indicate liquidity concerns, BUT some companies (like Apple) manage with <1.0 due to strong cash flow
- Above 3.0 may suggest inefficient capital use

## Analysis Framework:
1. ALWAYS compare metrics against INDUSTRY benchmarks first, not absolute standards
2. Consider the company's maturity stage and capital allocation strategy
3. High ROE + High Debt-to-Equity often means effective use of leverage
4. High ROE + Buybacks = shareholder-friendly capital returns
5. Be concise - provide insight, not just data repetition
6. When metrics seem contradictory, explain WHY (e.g., "low current ratio but strong cash flow")

## Communication Style:
- Lead with the most important insight
- Use 2-3 short paragraphs, not bullet lists unless specifically requested
- Provide context for "unusual" metrics (very high/low) before judging them
- Avoid phrases like "it's essential to consider" - just state the consideration directly
- No investment recommendations - objective analysis only

Always ground your analysis in the tool data, and explain your reasoning clearly.
"""

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
        
        # Prepare initial state with system prompt
        initial_state = {
            "messages": [
                SystemMessage(content=system_prompt),
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
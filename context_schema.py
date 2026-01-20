
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # The 'add_messages' function automatically handles appending new messages to history
    messages: Annotated[list, add_messages]




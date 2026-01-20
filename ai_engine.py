from langchain_ollama import ChatOllama
from tools import tools_list

# IMPORTANT: We use llama3.1 because it supports tool-calling natively
llm = ChatOllama(model="llama3.2:3b", temperature=0)

# Bind tools so the LLM knows they exist
llm_engine = llm.bind_tools(tools_list)
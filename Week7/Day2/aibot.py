from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv # used to store secret stuff like API keys or configuration values

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatOllama(model="qwen2:7b")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")



"""from langgraph.graph import StateGraph
from langchain_community.chat_models import ChatOllama
from typing import TypedDict

# define state
class AgentState(TypedDict):
    input: str
    output: str

llm = ChatOllama(model="qwen2:7b")

def chatbot(state):
    response = llm.invoke(state["input"])
    return {"output": response.content}

graph = StateGraph(AgentState)

graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.set_finish_point("chatbot")

app = graph.compile()

result = app.invoke({"input": "What is an AI agent?"})
print(result)"""
#  Imports
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END


#  1. STATE SCHEMA
# This defines what data (memory) flows in the graph
class ChatState(TypedDict):
    messages: List[BaseMessage]   # Stores conversation history
    context: str                  # Extra information (context)


#  2. REDUCER (Memory Management)
# Controls how messages are updated (append instead of overwrite)--cuts down the overwritting issue
def message_reducer(old_messages, new_messages):
    return old_messages + new_messages


#  3. NODE FUNCTION (logic)
def chatbot_node(state: ChatState):
    """
    This function:
    - Reads message history
    - Uses context
    - Generates response
    """

    messages = state["messages"]        # full chat history
    context = state["context"]          # extra context
    
    # get last user message
    user_input = messages[-1].content

    # simple response logic
    reply = f"[Context: {context}] → Echo: {user_input}"

    # return new AI message (gets merged by reducer)
    return {
        "messages": [AIMessage(content=reply)]
    }


#  4. BUILD GRAPH
builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot_node)

builder.set_entry_point("chatbot")
builder.add_edge("chatbot", END)


#  5. ADD REDUCER (IMPORTANT)
# Without this → messages will overwrite instead of storing history
builder.add_state_updater("messages", message_reducer)


#  6. COMPILE GRAPH
graph = builder.compile()


#  7. RUN (Conversation Simulation)
state = {
    "messages": [],                # initial empty memory
    "context": "Friendly assistant"
}

# ---- Turn 1 ----
state["messages"].append(HumanMessage(content="Hello"))
state = graph.invoke(state)

# ---- Turn 2 ----
state["messages"].append(HumanMessage(content="How are you?"))
state = graph.invoke(state)


#  8. PRINT FULL MEMORY (Message History)
print("\nConversation History:\n")
for msg in state["messages"]:
    print(msg.content)

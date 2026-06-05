from langchain_ollama import ChatOllama
from langchain_classic.memory import ConversationBufferMemory

llm = ChatOllama(model="llama3")

#session storage

sessions = {}

#chatbot functions
def get_session_memory(session_id):

    if session_id not in sessions:
        sessions[session_id] = ConversationBufferMemory()

    return sessions[session_id]

def chatbot(session_id, user_input):

    memory = get_session_memory(session_id)
    history = memory.load_memory_variables({})
    prompt = f"""
    Conversation History:
    {history}

    User:
    {user_input}
    """

    response = llm.invoke(prompt)
    memory.save_context(
        {"input": user_input},
        {"output": response.content}
    )

    return response.content


print(chatbot("user1", "My name is John"))
print(chatbot("user1", "What is my name?"))

print(chatbot("user2", "My name is Alice"))
print(chatbot("user2", "What is my name?"))

from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3")

def agent(question):
    print("Goal:", question)

    thought = llm.invoke(f"Think step by step to solve: {question}").content
    print("\nThought:", thought)

    answer = llm.invoke(f"Give final answer based on this reasoning:\n{thought}").content
    return answer

print(agent("What is 25 * 4 + 10?"))
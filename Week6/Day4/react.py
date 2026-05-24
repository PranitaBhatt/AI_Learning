from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3")

def calculator(expression):
    return str(eval(expression))

def react_agent(query):
    print("Question:", query)

    thought = llm.invoke(f"What should I do step by step?\n{query}").content
    print("\nThought:", thought)

    if "calculate" in thought.lower():
        expression = llm.invoke(f"Extract math expression from: {query}").content
        result = calculator(expression)
        print("\nAction: Calculator")
        print("Observation:", result)

        final = llm.invoke(f"Final answer using result {result}").content
    else:
        final = llm.invoke(query).content

    return final

print(react_agent("What is 45 * 2?"))
